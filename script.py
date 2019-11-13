import pymysql
import pymysql.cursors
import random

connection = pymysql.connect(
    host="localhost", user="root", db="station", autocommit=True
)

etypes = ["manager", "cleaning_staff", "station_master", "ticket_checker", "engineer"]
btypes = ["enquiry", "food_store", "ticket_counter", "toilet"]


def render_menu(items):
    while True:
        print("-" * 76)
        for idx, i in enumerate(items):
            print(idx + 1, i)
        print(len(items) + 1, "Back")
        ch = int(input("Enter a choice: "))
        if not 1 <= ch <= len(items) + 1:
            print("Invalid choice")
            continue
        if ch == len(items) + 1:
            return False
        list(items.values())[ch - 1]()
        return True


def generate_ticket():
    train_number = input("Enter train number: ")
    berth = input("Enter berth: (L/U/M): ")
    coach = input("Enter coach number: ")
    journey_date = input("Enter journey date: ")
    cost = random.randint(1000, 2000)
    sql = "insert into ticket values (%s, 0, %s, %s, %s, %s)"
    try:
        with connection.cursor() as cur:
            cur.execute(sql, (train_number, berth, coach, journey_date, cost))
    except Exception as e:
        print(e)


def cancel_ticket():
    tno = input("Enter ticket number: ")
    sql = "delete frm ticket where ticket_number = %s"
    try:
        with connection.cursor() as cur:
            cur.execute(sql, (tno,))
    except Exception as e:
        print(e)


def view_all_tickets():
    try:
        with connection.cursor() as cur:
            cur.execute("show columns from ticket")
            for r in cur.fetchall():
                print(r[0], end=" | ")
            print()
            cur.execute("select * from ticket")
            for r in cur.fetchall():
                print(r)
    except Exception as e:
        print(e)


def ticket_report():
    start = input("enter start date: ")
    end = input("enter end date: ")

    try:
        with connection.cursor() as cur:
            cur.execute(
                "select * from ticket where journey_date between %s and %s",
                (start, end),
            )
            c = 0
            for r in cur.fetchall():
                print(r)
                c += 1
            print("total of %d tickets were sold" % c)
            cur.execute(
                "select train_number from ticket group by train_number order by count(*) desc"
            )
            print("most tickets sold for the train number: ")
            print(cur.fetchone())
    except Exception as e:
        print(e)


def ticket_counter_view():
    menu = {
        "Generate new ticket": generate_ticket,
        "Cancel ticket": cancel_ticket,
        "View all tickets": view_all_tickets,
        "ticket report": ticket_report,
    }
    while render_menu(menu):
        pass


def add_train():
    sql = "insert into train values (%s, %s, %s, %s, NULL)"
    train_number = input("Enter train number: ")
    train_name = input("Enter train name: ")
    train_type = input("Enter train type: (superfast/local/express) ")
    num_coach = input("Enter number of coaches: ")
    try:
        with connection.cursor() as cur:
            cur.execute(sql, (train_number, train_name, train_type, num_coach))
    except Exception as e:
        print(e)


def view_trains():
    sql = "select * from train"
    try:
        with connection.cursor() as cur:
            cur.execute(sql)
            for row in cur.fetchall():
                print(row)
    except Exception as e:
        print(e)


def remove_train():
    sql = "delete from train where train_number = %s"
    train_number = input("Enter train number: ")
    try:
        with connection.cursor() as cur:
            cur.execute(sql, (train_number,))
    except Exception as e:
        print(e)


def add_timetable():
    sql = """insert into time_table (train_number, platform_number, arrival_time, departure_time) 
            values (%s, %s, %s, %s)"""
    train_number = input("enter train number: ")
    platform_number = input("enter platform number: ")
    arrival_time = input("enter arrival time (HH:MM): ")
    departure_time = input("enter departure time (HH:MM): ")
    try:
        with connection.cursor() as cur:
            cur.execute(
                sql, (train_number, platform_number, arrival_time, departure_time)
            )
    except Exception as e:
        print(e)


def generate_timetable():
    sql = "select train.train_number, train_name, platform_number, cast(arrival_time as char), cast(departure_time as char) from time_table join train on time_table.train_number = train.train_number order by arrival_time asc"
    try:
        with connection.cursor() as cur:
            # cur.execute("show columns from time_table")
            # for row in cur.fetchall():
            #     print(row[0], end=" | ")
            # print()
            cur.execute(sql)
            for row in cur.fetchall():
                print(row)
    except Exception as e:
        print(e)


def station_master_view():
    menu = {
        "Add new train": add_train,
        "Remove train": remove_train,
        "View train list": view_trains,
        "Add timetable entry": add_timetable,
        "Generate timetable": generate_timetable,
    }
    while render_menu(menu):
        pass


def add_employee():
    name = input("Enter employee name: ")
    dob = input("Enter employee dob (YYYY-MM-DD): ")
    manager = input("Enter manager ID (can be NULL): ")
    salary = input("Enter employee salary: ")
    t = input("Enter employee type: (%s): " % "/".join(etypes))

    if t not in etypes:
        print("invalid employee type")
        return

    sql = "insert into employee (name, dob, salary, manager_id) values (%s, %s, %s, %s)"

    try:
        with connection.cursor() as cur:
            cur.execute(
                sql, (name, dob, salary, manager if manager.lower() != "null" else None)
            )
            cur.execute("insert into %s values (last_insert_id())" % t)
    except Exception as e:
        print(e)


def fire_employee():
    sql = "delete from employee where employee_id = %s"
    eid = input("Enter employee id: ")
    try:
        with connection.cursor() as cur:
            cur.execute(sql, (eid,))
    except Exception as e:
        print(e)


def view_employees():
    sql = "select * from employee"
    try:
        with connection.cursor() as cur:
            cur.execute("show columns from employee;")
            for row in cur.fetchall():
                print(row[0], end=" | ")
            print()
            for t in etypes:
                print("employees of type %s" % t)
                sql = (
                    "select * from %s join employee on %s.employee_id = employee.employee_id"
                    % (t, t)
                )
                cur.execute(sql)
                for row in cur.fetchall():
                    print(row)
    except Exception as e:
        print(e)


def change_employee_type():
    try:
        eid = input("enter employee id: ")
        new = input(
            "enter new employee role: (manager/engineer/cleaning_staff/station_master/ticket_checker)"
        )
        if new not in etypes:
            print("invalid employee type")
            return
        with connection.cursor() as cur:
            for table in etypes:
                cur.execute(
                    "delete from {} where employee_id = %s".format(table), (eid,)
                )
            cur.execute("insert into {} values (%s)".format(new), (eid,))
    except Exception as e:
        print(e)


def manager_view():
    menu = {
        "Hire employee": add_employee,
        "Fire employee": fire_employee,
        "View employee list": view_employees,
        "Change employee role": change_employee_type,
    }
    while render_menu(menu):
        pass


def add_platform():
    sql = "insert into platform (platform_no, len) values (%s, %s)"
    pno = input("enter platform number: ")
    length = input("enter platform length: ")

    try:
        with connection.cursor() as cur:
            cur.execute(sql, (pno, length))
    except Exception as e:
        print(e)


def train_maintenance():
    tno = input("enter train number: ")
    try:
        with connection.cursor() as cur:
            cur.execute(
                "update train set last_maintenance = curdate() where train_number = %s",
                (tno,),
            )
    except Exception as e:
        print(e)


def building_maintenance():
    bno = input("enter building number: ")
    try:
        with connection.cursor() as cur:
            cur.execute(
                "update building set last_maintenance = curdate() where building_id = %s",
                (bno,),
            )
    except Exception as e:
        print(e)


def cleaning_staff_view():
    menu = {
        "train maintenance": train_maintenance,
        "building maintenance": building_maintenance,
    }
    while render_menu(menu):
        pass


def add_building():
    t = input("Enter building type: (%s): " % "/".join(btypes))

    if t not in btypes:
        print("invalid building type")
        return

    sql = "insert into building values ()"

    try:
        with connection.cursor() as cur:
            cur.execute(sql)
            cur.execute("insert into %s values (last_insert_id())" % t)
    except Exception as e:
        print(e)


def list_buildings():
    try:
        with connection.cursor() as cur:
            print("building id | last maintenance")
            for b in btypes:
                print("building type %s" % b)
                cur.execute(
                    "select building.building_id, cast(last_maintenance as char) from %s join building on %s.building_id = building.building_id"
                    % (b, b)
                )
                for r in cur.fetchall():
                    print(r)
    except Exception as e:
        print(e)


def list_platforms():
    try:
        with connection.cursor() as cur:
            cur.execute("show columns from platform")
            for row in cur.fetchall():
                print(row[0], end=" | ")
            print()
            cur.execute("select * from platform")
            for row in cur.fetchall():
                print(row)
    except Exception as e:
        print(e)


def entry():
    print("Choose a user type:")
    menu = {
        "Manager": manager_view,
        "Ticket Counter": ticket_counter_view,
        "Station Master": station_master_view,
        "Cleaning Staff": cleaning_staff_view,
        "Add platform": add_platform,
        "show platforms": list_platforms,
        "Add building": add_building,
        "show building list": list_buildings,
    }
    while render_menu(menu):
        pass


if __name__ == "__main__":
    entry()
