from django.db import models
import django_tables2 as tables

class Ticket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    t_opened = models.DateTimeField(auto_now_add=True, verbose_name='Date Opened')
    t_status = models.ForeignKey('Status', on_delete=models.CASCADE)
    t_subject = models.CharField(max_length=100, verbose_name='Subject')
    t_body = models.TextField(verbose_name='Ticket Summary')
    t_closed = models.DateTimeField(verbose_name='Date Closed', null=True, blank=True)
    t_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    c_info = models.ForeignKey('Customer', on_delete=models.CASCADE)
    tech_info = models.ForeignKey('Technician', on_delete=models.CASCADE)

    def __str__(self):
        return self.t_subject

class Technician(models.Model):
    te_name = models.CharField(max_length=150, verbose_name='Technician Name')
    te_id = models.CharField(max_length=100, verbose_name='Assigned Technician')
    te_phone = models.CharField(max_length=14, verbose_name='Technician Phone Number')
    te_email = models.CharField(max_length=111, verbose_name='Technician Email')

    def __str__(self):
        return self.te_name
    
class Customer(models.Model):
    c_name = models.CharField(max_length=150, verbose_name='Customer Name')
    c_id = models.CharField(max_length=100, verbose_name='Customer ID')
    c_phone = models.CharField(max_length=14, verbose_name='Customer Phone Number')
    c_email = models.CharField(max_length=111, verbose_name='Customer Email')

    def __str__(self):
        return self.c_name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category')

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Status')

    def __str__(self):
        return self.name

class TicketTable(tables.Table):
    pk = tables.Column(verbose_name='Ticket ID')
    class Meta:
        model = Ticket
        fields = ('t_opened', 'c_info.c_name', 't_subject', 't_status.name', 'tech_info.te_id', 't_closed', 'pk')
        template_name = 'tables.html'