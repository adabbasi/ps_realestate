from datetime import date, timedelta, datetime
from odoo import fields, models, api
from . import estate_property
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"


    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(string="Status", selection=[('accepted','Accepted'), ('rejected','Rejected')])
    property_id = fields.Many2one('estate.property', string="Property" , required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)

    date_deadline = fields.Date(string="Valid till", compute="_compute_deadline")
    validity = fields.Integer(string="Days valid", default=7)

    property_type_id = fields.Many2one(related="property_id.property_type_id",  stored=True)

    _sql_constraints = [('chk_price', 'CHECK(price >= 0)', 'The offer price should not be a negative value')]

    @api.depends('validity')
    def _compute_deadline(self):
        for rec in self:
            rec.date_deadline = datetime.now() + timedelta(rec.validity)

    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer_id = rec.partner_id
            rec.property_id.state = rec.status

    def action_rejected(self):
        for rec in self:
            rec.status = 'rejected'

    @api.model
    def create(self, vals_list):
        self.property_id.state = 'offer'
        prop_id = vals_list['property_id']
        curr_price= vals_list['price']
        print(prop_id,curr_price)
        prop  = self.env['estate.property'].browse(prop_id).mapped('offer_ids').mapped('price')
        if prop:
         maxoffer = max(prop)
         if curr_price < maxoffer:
            raise UserError("New offer cannot be lower than: " + format(maxoffer,","))
        return super(EstatePropertyOffer, self).create(vals_list)

