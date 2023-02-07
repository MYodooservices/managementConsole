
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

    #many2One =  fields.Char("City", related='many2One_id.name') 

    def _get_selection(self):
        #journal_obj = self.pool.get('ir.model.fields')
        #journal_ids = journal_obj.search(cr, uid, [], context=context)

        contactFields = self.env["ir.model.fields"].search([("model", "=", "res.partner")])

        lst = []
        for contactFields in contactFields:
            lst.append((contactFields.name, contactFields.name))
        
        return lst
    
    def _get_filtered_selection(self):
        #journal_obj = self.pool.get('ir.model.fields')
        #journal_ids = journal_obj.search(cr, uid, [], context=context)

        contactFields = self.env["ir.model.fields"].search([("model", "=", "res.partner")])

        lst = []
        for contactFields in contactFields:
            lst.append((contactFields.name, contactFields.name))
        
        return lst
        
      
    field_boolean = fields.Boolean('boolean')    

    field_selection = fields.Many2one('ir.model.fields', string="field", create=False,  domain=[("model", "=", "res.partner")] )  #fields.Selection(_get_selection, 'field name')

    

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

            if(self.state == "boolean"):
                if(not self.field_boolean):
                    other_model_record.write({self.field_selection.name: False})
                else:
                    other_model_record.write({self.field_selection.name: True})
            elif(field_type == 'many2one'):
                other_model_record.write({self.field_selection.name: int(self.field_writeValue)})
            else:
                other_model_record.write({self.field_selection.name: self.field_writeValue})
            #print(len(other_model_record))

            #for user in users:
            #    print("user: ", user)

    
    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('many2One', 'many2One'),
            ('boolean', 'Boolean'),
            ('loaded', 'Loaded')
        ]

    @api.onchange('field_selection')
    def check_field_type(self):
        if(self.field_selection.ttype == "boolean"):
            self.state = 'boolean'
        else:
            self.state = 'start'

    def state_exit_start(self):
        self.update_users()
    
    def state_exit_boolean(self):
        self.update_users()
   
        
  
    
    
   
