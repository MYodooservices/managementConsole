
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odoo import models, fields
import base64






class optout(models.TransientModel):
    _name = 'mmc.optout'
    csv_file = fields.Binary(string='', help="", store=True)
    file_name = fields.Char(string='')

    edit_model = fields.Char(string='')

    field_name = fields.Char(string='')
    field_operator = fields.Char(string='')
    field_value = fields.Char(string='')

    
    field_writeField = fields.Char(string='')
    field_writeValue = fields.Char(string='')

    def _get_selection(self):
        #journal_obj = self.pool.get('ir.model.fields')
        #journal_ids = journal_obj.search(cr, uid, [], context=context)

        contactFields = self.env["ir.model.fields"].search([("model", "=", "res.partner")])

        lst = []
        for contactFields in contactFields:
            lst.append((contactFields.name, contactFields.name))
        
        return lst
        
      

    field_selection = fields.Selection(_get_selection, 'selection')

      

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

            other_model_record.write({self.field_selection: self.field_writeValue})
            #print(len(other_model_record))

            #for user in users:
            #    print("user: ", user)

    
   
    
        
  
    
    
   
