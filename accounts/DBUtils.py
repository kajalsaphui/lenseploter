from . import Defaults
import pyodbc


def DB_Execute_MS(sql_query, action):

    #Defaults.logger("Entering -> | DB_Insert() |", level = "info")

    # Open database connection
    #db = pymssql.connect(host ='ADAS\SQLEXPRESS2019',user ='sa',password ='Paromita@19',database ='vrx_sfts')
    db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms+';DATABASE='+Defaults.schema_ms+';UID='+Defaults.user_ms+';PWD='+ Defaults.password_ms)
    #print(db)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    if action == "insert":
        try:
                # Execute the SQL command
            status = cursor.execute(sql_query)
            print("status",status)
                # Commit your changes in the database
            db.commit()
            return status
        except:
            # Rollback in case there is any error
            db.rollback()
            Defaults.logger("DB INSERT FAILED", sql_query, "debug")
            return False

    elif action == "fetch":
        try:
                # Execute the SQL command
            cursor.execute(sql_query)
            # fetch all the content from the query
            fetched_content = cursor.fetchall()
        #return the content
            return fetched_content

        except Exception as e:
            # log the exception
            Defaults.logger("DB FETCH EXCEPTION", e, "debug")
            Defaults.logger("DB FETCH EXCEPTION sql", sql_query, "debug")
            return False
    
    
    # elif action == "update":
    #     try:
    #         # Execute the SQL command
    #         status = cursor.execute(sql_query,data)
    #         # Commit your changes in the database
    #         db.commit()
    #         return status
    #     except:
    #         # Rollback in case there is any error
    #         db.rollback()
    #         Defaults.logger("DB INSERT FAILED", sql_query, "debug")
    #         return False



    elif action == "delete":
        try:
    # cursor   
            cursor.execute(sql_query)   
    # commit
            db.commit()    
    # total number of rows inserted  
        except pyodbc.connector.Error as err:   
            print("Error:", err.message)
            db.rollback()
            Defaults.logger("DB delet FAILED", sql_query, "debug")
            return False
    # close connection

    return True


def DB_Update_MS(sql_query, action,data):

    #Defaults.logger("Entering -> | DB_Insert() |", level = "info")

    # Open database connection
    db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms+';DATABASE='+Defaults.schema_ms+';UID='+Defaults.user_ms+';PWD='+ Defaults.password_ms)
    #print(db)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    if action == "insert":
        try:
            # Execute the SQL command
            status = cursor.execute(sql_query,data)
            # Commit your changes in the database
            db.commit()
            print("Status:",status)
            return status
        except:
            # Rollback in case there is any error
            db.rollback()
            Defaults.logger("DB INSERT FAILED", sql_query, "debug")
            return False

    return True
#==============================================================================================================




def DB_Execute_MS_Axapta(sql_query, action):

    #Defaults.logger("Entering -> | DB_Insert() |", level = "info")

    # Open database connection
    #db = pymssql.connect(host ='ADAS\SQLEXPRESS2019',user ='sa',password ='Paromita@19',database ='vrx_sfts')
    db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms_axcepta+';DATABASE='+Defaults.schema_ms_axcepta+';UID='+Defaults.user_ms_axcepta+';PWD='+ Defaults.password_ms_axcepta)
    #print(db)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    if action == "insert":
        try:
                # Execute the SQL command
            status = cursor.execute(sql_query)
            print("status",status)
                # Commit your changes in the database
            db.commit()
            return status
        except:
            # Rollback in case there is any error
            db.rollback()
            Defaults.logger("DB INSERT FAILED", sql_query, "debug")
            return False

    elif action == "fetch":
        try:
                # Execute the SQL command
            cursor.execute(sql_query)
            # fetch all the content from the query
            fetched_content = cursor.fetchall()
        #return the content
            return fetched_content

        except Exception as e:
            # log the exception
            Defaults.logger("DB FETCH EXCEPTION", e, "debug")
            Defaults.logger("DB FETCH EXCEPTION sql", sql_query, "debug")
            return False
    
    
    # elif action == "update":
    #     try:
    #         # Execute the SQL command
    #         status = cursor.execute(sql_query,data)
    #         # Commit your changes in the database
    #         db.commit()
    #         return status
    #     except:
    #         # Rollback in case there is any error
    #         db.rollback()
    #         Defaults.logger("DB INSERT FAILED", sql_query, "debug")
    #         return False



    elif action == "delete":
        try:
    # cursor   
            cursor.execute(sql_query)   
    # commit
            db.commit()    
    # total number of rows inserted  
        except pyodbc.connector.Error as err:   
            print("Error:", err.message)
            db.rollback()
            Defaults.logger("DB delet FAILED", sql_query, "debug")
            return False
    # close connection

    return True


def DB_Update_MS_Axapta(sql_query, action,data):

    #Defaults.logger("Entering -> | DB_Insert() |", level = "info")

    # Open database connection
    db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms_axcepta+';DATABASE='+Defaults.schema_ms_axcepta+';UID='+Defaults.user_ms_axcepta+';PWD='+ Defaults.password_ms_axcepta)
    #print(db)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    if action == "insert":
        try:
            # Execute the SQL command
            status = cursor.execute(sql_query,data)
            # Commit your changes in the database
            db.commit()
            print("Status:",status)
            return status
        except:
            # Rollback in case there is any error
            db.rollback()
            Defaults.logger("DB INSERT FAILED", sql_query, "debug")
            return False

    return True