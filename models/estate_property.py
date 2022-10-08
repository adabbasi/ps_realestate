from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _rec_name = "prop_name"
    _order = "id desc"

    prop_name = fields.Char(string="Title", required=True)
    prop_description = fields.Text(string="Address")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=str(date.today()+relativedelta(months=+3)))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area(sqm)")
    garden_orient = fields.Selection(string="Garden orientation",
                                     selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                ('west', 'West')])
    state = fields.Selection([('new', 'New'), ('offer', 'Offer received'), ('accepted', 'Offer accepted'), ('cancel', 'Cancelled'), ('sold', 'Sold')], default='new', string="State", required=True)
    active = fields.Boolean(string="Active", default=True)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", index=True, tracking=True,
                                     default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer")

    property_tag_ids = fields.Many2many('estate.property.tag', string="Property tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    tot_area = fields.Integer(string="Total area", compute="_compute_tot_area")
    best_price = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [('chk_expected_price','CHECK(expected_price >= 0)', 'The expected price should not be a negative value'),
                        ('chk_selling_price', 'CHECK(selling_price >= 0)',  'The selling price should not be a negative value')
                       ]

    @api.constrains('selling_price')
    def _check_sell_price(self):
        for record in self:
            chk_price = 0.9 * record.expected_price
            if record.selling_price < chk_price and record.selling_price !=0:
                raise ValidationError("The selling price cannot be less than 90% of Expected Price")

    @api.depends('living_area', 'garden_area')
    def _compute_tot_area(self):
        for rec in self:
            rec.tot_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:

          result = rec.offer_ids.mapped('price')

          if result:
           if rec.state == 'new':
            rec.state = 'offer'
           rec.best_price = max(result)
          else:
           # rec.state = 'new'
           rec.best_price = 0


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orient = 'north'
        else:
            self.garden_area = 0
            self.garden_orient = ''

    def action_sold(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError('Cannot sell cancelled property')
            else:
                rec.state = 'sold'


    def action_cancel(self):
     for rec in self:
        if rec.state == 'sold':
            raise UserError('Cannot cancel sold property')
        else:
            rec.state = 'cancel'
            rec.active = False

    @api.ondelete(at_uninstall=False)
    def _unlink_chkstate(self):
        for rec in self:
            if (rec.state != 'new' and  rec.state != 'cancel'):
                raise UserError('Cannot delete property in this state!')


