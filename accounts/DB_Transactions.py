from . import DBUtils
from . import Defaults
def get_all_nodes():
    Defaults.logger("Entering -> | get_all_nodes() |", level = "info")    
    try:
        sql_query = "SELECT * FROM vrx_SFTS_node WHERE status = 1"    
        DBcontent = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(DBcontent)
        Defaults.logger("Exiting -> | get_all_nodes() |", level = "info")
        return DBcontent
    except:
        Defaults.logger("DATABASE OPERATION COULDN'T BE PERFORMED", "", level = "warning")
        Defaults.logger("Exiting -> | get_all_nodes() |", level = "info")
        return None


def get_all_orders():
    Defaults.logger("Entering -> | get_all_orders() |", level = "info")    
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM RXNetOrder_Webshop"
        # sql_query = "SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where Entry_date < GETDATE()-180 order by Entry_date DESC"     
        DBcontent = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(DBcontent)
        Defaults.logger("Exiting -> | get_all_orders() |", level = "info")
        return DBcontent
    except:
        Defaults.logger("DATABASE OPERATION COULDN'T BE PERFORMED", "", level = "warning")
        Defaults.logger("Exiting -> | get_all_orders() |", level = "info")
        return None

def get_all_orders_by_castomer(customer_code):
    Defaults.logger("Entering -> | get_all_orders_by_castomer() |", level = "info")
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM RXNetOrder_Webshop WHERE POHD_CUST_CD ='%s'"%(customer_code)
        # sql_query="SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where POAD_CUST_CD ='%s' AND Entry_date < GETDATE()-180 order by Entry_date DESC"%(customer_code)  
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_orders_by_castomer() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_by_castomer() |", level = "error")
        return None

# anirudha=========================

def get_all_orders_by_oci_castomer(oci_no,customer_code):
    Defaults.logger("Entering -> | get_all_orders_by_oci_castomer() |", level = "info")
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM RXNetOrder_Webshop WHERE OCI_NO='%s' AND POHD_CUST_CD ='%s'"%(oci_no,customer_code)
        # sql_query="SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where POAD_CUST_CD ='%s' AND Entry_date < GETDATE()-180 order by Entry_date DESC"%(customer_code)  
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_orders_by_oci_castomer |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_by_oci_castomer() |", level = "error")
        return None

def get_all_orders_by_oci_entrydate(day,month,year,customer_code):
    Defaults.logger("Entering -> | get_all_orders_by_oci_entrydate() |", level = "info")
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM RXNetOrder_Webshop WHERE  POHD_CUST_CD='%s' AND DAY(ENTRY_DATE)='%d' AND MONTH(ENTRY_DATE)= '%d' AND YEAR(ENTRY_DATE)='%s'"%(customer_code,int(day),int(month),year)
        # sql_query="SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where POAD_CUST_CD ='%s' AND Entry_date < GETDATE()-180 order by Entry_date DESC"%(customer_code)
        print(sql_query)  
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        # print(res)
        Defaults.logger("Exiting <- | get_all_orders_by_oci_entrydate() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_by_oci_entrydate() |", level = "error")
        return None

def get_all_orders_filter_by_entrydate(entry_year,entry_month,customer_code):
    Defaults.logger("Entering -> | get_all_orders_filter_by_entrydate() |", level = "info")
    # date_time_obj = datetime.strptime(entry_date, '%d/%m/%y %H:%M:%S')
    # print ("The type of the date is now",  type(date_time_obj))
    # print ("The date is", date_time_obj)
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM RXNetOrder_Webshop WHERE  POHD_CUST_CD='%s' AND MONTH(ENTRY_DATE)= '%d' AND YEAR(ENTRY_DATE)='%s'"%(customer_code,int(entry_month),entry_year)
        # sql_query="SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where POAD_CUST_CD ='%s' AND Entry_date < GETDATE()-180 order by Entry_date DESC"%(customer_code)  
        print(sql_query)
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_orders_filter_by_entrydate() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_filter_by_entrydate() |", level = "error")
        return None

def get_all_orders_filter_by_ref_no_val(ref_no,customer_code):
    Defaults.logger("Entering -> | get_all_orders_filter_by_ref_no_val() |", level = "info")
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM RXNetOrder_Webshop WHERE  POHD_SOURCE_REF ='%s' AND POHD_CUST_CD='%s'"%(ref_no,customer_code)
        # sql_query="SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where POAD_CUST_CD ='%s' AND Entry_date < GETDATE()-180 order by Entry_date DESC"%(customer_code)  
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_orders_filter_by_ref_no_val() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_filter_by_ref_no_val() |", level = "error")
        return None

# anirudha=============================

def get_tracevalue(oci_no):
    Defaults.logger("Entering -> | get_tracevalue() |", level = "info")
    try:
        sql_query = "SELECT TOP 1 NON_TRACER FROM RXNetOrder_Webshop WHERE OCI_NO ='%s'"%(oci_no) 
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_tracevalue() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_tracevalue() |", level = "error")
        return None


# ===============anirudha 20 july===============
def get_all_year_history(customer_code):
    Defaults.logger("Entering -> | get_all_year_history() |", level = "info")
    try:
        sql_query = "select distinct YEAR(entry_date) AS [YEAR] from RXNetOrder_Webshop WHERE POHD_CUST_CD='%s' ORDER BY YEAR(entry_date)"%(customer_code)
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_year_history() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_year_history() |", level = "error")
        return None

def get_month_by_year(year,customer_code):
    Defaults.logger("Entering -> | get_month_by_year() |", level = "info")
    try:
        sql_query = "select distinct LEFT(DATENAME(MONTH,entry_date),10) AS [MONTHNAME], MONTH(entry_date)[MONTH] from RXNetOrder_Webshop WHERE  POHD_CUST_CD='%s' AND YEAR(entry_date)='%s' ORDER BY MONTH(entry_date)"%(customer_code,year)
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_month_by_year() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_month_by_year() |", level = "error")
        return None


#========================vrxlab lab view===========================

def Cridential_mapping_vrxlab(customer_code):
    Defaults.logger("Entering -> | Cridential_mapping_vrxlab() |", level = "info")
    try:
        sql_query = "select Table_name  from accounts_master  WHERE Cust_code='%s'"%(customer_code)
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | Cridential_mapping_vrxlab() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | Cridential_mapping_vrxlab() |", level = "error")
        return None

# def Cridential_mapping_vrxlab_ref_cast_code(ref_customer_code):
#     print(ref_customer_code)
#     Defaults.logger("Entering -> | Cridential_mapping_vrxlab_ref_cast_code() |", level = "info")
#     # try:
#     sql_query = "select top 1 Table_name  FROM accounts_master  WHERE Ref_cust_code ='%s'"%(ref_customer_code)
#     res = DBUtils.DB_Execute_MS(sql_query, "fetch")
#     print(res)
#     Defaults.logger("Exiting <- | Cridential_mapping_vrxlab_ref_cast_code() |", level = "info")
#     return res
#     # except:
#         # Defaults.logger("Exiting <- | Cridential_mapping_vrxlab_ref_cast_code() |", level = "error")
#         # return None

def get_all_orders_by_oci_vrx_labworker(table_name,oci_no):
    print(table_name)
    print(oci_no)
    Defaults.logger("Entering -> | get_all_orders_by_oci_castomer_vrx_labworker() |", level = "info")
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM %s WHERE OCI_NO='%s'"%(table_name,oci_no)
        print(sql_query)
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_orders_by_oci_castomer_vrx_labworker |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_by_oci_castomer_vrx_labworker() |", level = "error")
        return None

def get_all_orders_by_ref_vrx_labworker(table_name,ref_no):
    Defaults.logger("Entering -> | get_all_orders_by_oci_castomer_vrx_labworker() |", level = "info")
    try:
        sql_query = "SELECT POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,convert(varchar(10),Entry_date,105) as Entry_date FROM '%s' WHERE POHD_SOURCE_REF='%s'"%(table_name,ref_no)
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_all_orders_by_oci_castomer_vrx_labworker |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_by_oci_castomer_vrx_labworker() |", level = "error")
        return None

def get_OMA_DATA(oci_no):
# def get_OMA_DATA():
    Defaults.logger("Entering -> | get_OMA_DATA() |", level = "info")
    try:
        sql_query = "SELECT TOP 1 OMA_DATA FROM RXNetOrder_Webshop WHERE OCI_NO ='%s'"%(oci_no)
        # sql_query = "SELECT TOP 1 OMA_DATA FROM RXNetOrder_Webshop WHERE OCI_NO ='EXP/129058/18'" 
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_OMA_DATA() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_OMA_DATA() |", level = "error")
        return None

def get_NON_TRACE_DATA(oci_no):
# def get_OMA_DATA():
    Defaults.logger("Entering -> | get_NON_TRACE_DATA() |", level = "info")
    try:
        sql_query = "SELECT TOP 1 NON_TRACER FROM RXNetOrder_Webshop WHERE OCI_NO ='%s'"%(oci_no)
        # sql_query = "SELECT TOP 1 NON_TRACE FROM RXNetOrder_Webshop WHERE OCI_NO ='EXP/129058/18'" 
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        print(res)
        Defaults.logger("Exiting <- | get_NON_TRACE_DATA() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_NON_TRACE_DATA() |", level = "error")
        return None

#======================================================================================

def get_all_orders_report_entrydate(day,month,year,day2,month2,year2,customer_code):
    Defaults.logger("Entering -> | get_all_orders_by_oci_entrydate() |", level = "info")
    try:
        sql_query = "SELECT convert(varchar(10),Entry_date,105) [ORDERDATE],OCI_NO [OCINUMBER],POHD_ACCOUNT_CD [CUSTCODE],POHD_SOURCE_REF [REFNUMBER],RIGHT_POPR_PROD_CD [RECODE], RIGHT_POLN_COMM_DIAM [RECOMMDIA],RIGHT_POPR_REQ_DIAMETER [REREQDIA],RIGHT_POPR_SPHERE [RESPHERE],RIGHT_POPR_CYLINDER [RECYLINDER],RIGHT_POPR_AXIS [REAXIS],RIGHT_POPR_ADDITION [READDITION],RIGHT_POLN_QUANTITY [REQTY],RIGHT_POPR_REQ_BASE [REBASE],RIGHT_POPR_REQ_CT [RECT], RIGHT_POPR_REQ_ET [REET],RIGHT_POPR_PRISM_1 [REPRISM1],RIGHT_POPR_PRISM_DIR_1 [REPRISM1DIA],RIGHT_POPR_PRISM_2 [REPRISM2],RIGHT_POPR_PRISM_DIR_2 [REPRISM2DIA],RIGHT_POPR_PD [REPD], RIGHT_POPR_NPD [RENPD],RIGHT_POPR_HEIGHT [REHEIGHT],LEFT_POPR_PROD_CD [LECODE], LEFT_POLN_COMM_DIAM [LECOMMDIA],LEFT_POPR_REQ_DIAMETER [LEREQDIA],LEFT_POPR_SPHERE [LESPHERE],LEFT_POPR_CYLINDER [LECYLINDER],LEFT_POPR_AXIS [LEAXIS],LEFT_POPR_ADDITION [LEADDITION],LEFT_POLN_QUANTITY [LEQTY],LEFT_POPR_REQ_BASE [LEBASE],LEFT_POPR_REQ_CT [LECT], LEFT_POPR_REQ_ET [LEET],LEFT_POPR_PRISM_1 [LEPRISM1],LEFT_POPR_PRISM_DIR_1 [LEPRISM1DIA],LEFT_POPR_PRISM_2 [LEPRISM2],LEFT_POPR_PRISM_DIR_2 [LEPRISM2DIA],LEFT_POPR_PD [LEPD], LEFT_POPR_NPD [LENPD],LEFT_POPR_HEIGHT [LEHEIGHT],SERVICE1_POLN_PROD_CD [COATINGCOADE],SERVICE1_SOURCE_PROD_DESC [COATINGDESC], SERVICE2_POLN_PROD_CD [TINTCOADE],SERVICE2_SOURCE_PROD_DESC [TINTDESC],POTR_A [BOXA],POTR_B [BOXB], POTR_DBL [DBL],POTR_FRAME [FRAMETYPE],VERTEX_DIST [VERTEXDIST], WRAPANGLE [WRAPANGLE], PANTOANGLE [PANTOANGLE],SPLINSTRUCTION [SPLINSTRUCTION], EDGINGTYPE [EDGINGTYPE] FROM RXNetOrder_Webshop WHERE  POHD_CUST_CD='%s'AND Entry_date Between '%s' + '%s' + '%s' And '%s' + '%s' + '%s'"%(customer_code,year,month,day,year2,month2,day2)
        # sql_query="SELECT top 100 POHD_CUST_CD,POHD_APPLICATION_NAME,POHD_SOURCE_REF,OCI_NO,POHD_PATIENT_FIRST_NAME,Entry_date FROM BKP_RXNetOrder With (NOLOCK) where POAD_CUST_CD ='%s' AND Entry_date < GETDATE()-180 order by Entry_date DESC"%(customer_code)
        print(sql_query)  
        res = DBUtils.DB_Execute_MS(sql_query, "fetch")
        # print(res)
        Defaults.logger("Exiting <- | get_all_orders_by_oci_entrydate() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_all_orders_by_oci_entrydate() |", level = "error")
        return None

def get_Extra_DATA_Axcepta(oci_no):
# def get_OMA_DATA():
    # Defaults.logger("Entering -> | get_Extra_DATA_Axcepta() |", level = "info")
    try:
        # print(oci_no)
        sql_query ="SELECT LELENSNAME,LEREFINDEX,LEFOCALITY,LELENSMAT,CUSTLELENSNAME as LE_PRODUCT_DESCRIPTION,RELENSNAME,OCINUMBER,REREFINDEX,REFOCALITY,RELENSMAT,CUSTRELENSNAME as RE_PRODUCT_DESCRIPTION FROM OCI_EXPORTFINAL WHERE OCINUMBER = '%s' AND PARTITION='5637144576' AND DATAAREAID='dub'"%(oci_no)
        # sql_query = "SELECT TOP 1 NON_TRACE FROM RXNetOrder_Webshop WHERE OCI_NO ='EXP/129058/18'" 
        res = DBUtils.DB_Execute_MS_Axapta(sql_query, "fetch")
        # print(res)
        # Defaults.logger("Exiting <- | get_Extra_DATA_Axcepta() |", level = "info")
        return res
    except:
        Defaults.logger("Exiting <- | get_Extra_DATA_Axcepta() |", level = "error")
        return None