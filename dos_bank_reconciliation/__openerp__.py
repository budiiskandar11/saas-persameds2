{
    "name" : "Bank Reconciliation",
    "version" : "1.0",
    "author" : "DATABIT",
    "category" : "Accounting",
    "website" : "http://www.databit.co.id",
    "description": """
    Bank Reconciliation Menu
    """,
    "depends" : [
                "account","dos_account_payment","report_xls"
                ],
    "init_xml" : [],
    "update_xml" : [
                    "bank_reconciliation_view.xml",
                    "report/bank_reconciliation_list_xls.xml",
                    "cash_opname_view.xml",
                    "report/report_bapuk.xml",
                    "bank_cash_summary_view.xml",
                    "report/cash_bank_summary_xls.xml",
                    #"bank_cash_summary_report.xml",
                    ],
    "active": False,
    "installable": True
}