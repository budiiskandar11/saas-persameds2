from openerp.osv import fields,osv

class hr_contract(osv.osv):
    _inherit = "hr.contract"
    
    _columns = {
        "overtime_allocation_amount" : fields.float("Overtime Allocation",digits=(16,2)),
        "latetime_deduction_amount" : fields.float("Latetime Deduction",digits=(16,2)),
        "meal_allowance_amount" : fields.float("Meal Allowance",digits=(16,2)),
        "allowance_amount" : fields.float("Allowance",digits=(16,2)),
        "extra_day_amount" : fields.float("Extra Day Allocation",digits=(16,2)),
        "absent_amount" : fields.float("Absent Deduction",digits=(16,2)),
        "extraday_working_hours":fields.many2one('resource.calendar',"Extra-day working hours"),
        'normal_days':fields.float("Normal Days",digits=(16,2)),
        
        "fasilitas_jabatan" : fields.float("Fasilitas Jabatan",digits=(16,2), help="Hitungan Take Homepay"),
        "tunjangan_khusus" : fields.float("Tunjangan Khusus",digits=(16,2), help="Non Hitungan Take Homepay"),
        "tunjangan_Perumahan" : fields.float("Tunjangan Perumahan",digits=(16,2), help="Non Hitungan Take Homepay"),
        "tunjangan_telephone" : fields.float("Tunjangan Telephone",digits=(16,2), help="Non Hitungan Take Homepay"),
        "tunjangan_self_manage" : fields.float("Self Manage",digits=(16,2), help="Non Hitungan Take Homepay"),
            }
    
hr_contract()