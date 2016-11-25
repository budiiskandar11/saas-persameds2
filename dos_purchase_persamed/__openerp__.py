{
    "name" : "Purchase",
    "version" : "1.0",
    "depends" : ["product",
                 "purchase",
                 "account",
                 "stock",
                 "report_webkit"
                 ],
    "author" : "DATABIT",
    "description": """Calculate Inventory Include Tax.
    """,
    "website" : "http://www.databit.co.id",
    "category" : "Custom/Purchase",
    "init_xml" : [],
    "demo_xml" : [],
    'test': [],
    "update_xml" : [
                    'purchase_inherit_view.xml',
                    'report/po_header_footer.xml',
                    'report/persamed_rfq.xml',
                    'report/rfq_report.xml',
                    #'security/account_security.xml',
                    #'security/ir.model.access.csv',
                    #'report/po_header_footer.xml',
                    #'report/pr_header_footer.xml',
                    #'report/po_report.xml',
                    #"wizard/purchase_requisition_line_view.xml",
                    #"purchase_requisition_view.xml",
                    #"purchase_requisition_workflow.xml",
                    #"purchase_sequence.xml",
                    #"purchase_view.xml",
                    #"stock_view.xml",
                    #"product_view.xml",
                    #"stock_view.xml",
                    #"purchase_view.xml",     
                    #"account_invoice_view.xml",
                    #"purchase_order_line_view.xml",
                    #'report/receiving_report.xml',
                    
                    
                    
       
    ],
    "active": False,
    "installable": True,
}