
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64
import json





class optout(models.TransientModel):
    _name = 'mmc.optout'
    _inherit = ['multi.step.wizard.mixin']
    

    csv_file = fields.Binary(string='', help="", store=True)
    file_name = fields.Char(string='')

    edit_model = fields.Char(string='')

    field_name = fields.Char(string='')
    field_operator = fields.Char(string='')
    field_value = fields.Char(string='')

    field_writeValue = fields.Char(string='field value')
    

    many2One_id = fields.Many2one('res.country', string="many2one", create=False) 

    
    #bulk update needed fields
    record_template = fields.Many2one('res.partner', 'name')
    field_selection = fields.Many2one('ir.model.fields', string="field", create=False,  domain=[("model", "=", "res.partner")] )  

    #many2One =  fields.Char("City", related='many2One_id.name') 

    def _get_selection(self):
        #journal_obj = self.pool.get('ir.model.fields')
        #journal_ids = journal_obj.search(cr, uid, [], context=context)

        contactFields = self.env["ir.model.fields"].search([("model", "=", "res.partner")])

        lst = []
        for contactFields in contactFields:
            lst.append((contactFields.name, contactFields.name))
        
        return lst
    
    global cnt
    cnt = 0
    global dynamic_list
    dynamic_list = []

    def _get_dynamic_selection(self):
        global cnt
        global dynamic_list


        for i in range(1,5):
            dynamic_list.append((str(cnt),str(i)))
            cnt=cnt+1

        return dynamic_list
    
    
    dynamic_selection = fields.Selection(_get_dynamic_selection, 'field name')
    
 
    


    def _get_filtered_selection(self):
        #journal_obj = self.pool.get('ir.model.fields')
        #journal_ids = journal_obj.search(cr, uid, [], context=context)

        contactFields = self.env["ir.model.fields"].search([("model", "=", "res.partner")])

        lst = []
        for contactFields in contactFields:
            lst.append((contactFields.name, contactFields.name))
        
        return lst
        
      
    field_boolean = fields.Boolean('boolean')    

    

    def bulk_update (self):
        print("bulk update")
        f = self.field_selection.name
        active_ids = self._context.get('active_ids', []) or []
        for record in self.env['res.partner'].browse(active_ids):
           

            #record.website = "manuelmarco.xyz"
            print("selected field: ")
            print(self.field_selection)
            print("selected record: ")
            print(self.record_template)
            print("field of record:")
            print(self.record_template[f])
            #record.parent_id = self.field_company_id.id

            
            #record._fields[f] = self.record_template._fields[f]
            record.write({f: self.record_template[f]}) #sset 
        


    def update_users(self):
        print("update users by csv file")
        print(self.csv_file)
        file = base64.b64decode(self.csv_file)
        if(file != False):
            records = file.decode().split('\n')
            other_model_record = self.env["res.partner"].search([("email", "in", records)])
            print("records found: ")
            print(len(other_model_record))
            
            #other_model_record = self.env[self.edit_model].search([(self.field_name, self.field_operator, self.field_value)])
            #other_model_record.write({self.field_writeField: self.field_writeValue})

            print("selected field:")
            print(self.field_selection)
            print("to:")
            print(self.field_writeValue)

            #ir_model_obj=self.env['ir.model.fields']
            #ir_model_field=ir_model_obj.search([('model','=','res.partner'),('name','=',self.field_selection)])
            
            field_type=self.field_selection.ttype
            #if field_type=='many2one':
                #show many2One field

            other_model_record.write({self.field_selection.name: self.field_writeValue})
            #print(len(other_model_record))

            #for user in users:
            #    print("user: ", user)

   
   
        
  
    
    
   
