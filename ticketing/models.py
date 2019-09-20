from django.db import models

class Ticket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    t_opened = models.DateTimeField(auto_now_add=True)
    t_status = models.ForeignKey('Status', on_delete=models.CASCADE)
    t_subject = models.CharField(max_length=100)
    t_body = models.TextField()
    t_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    c_info = models.ForeignKey('Customer', on_delete=models.CASCADE)
    tech_info = models.ForeignKey('Technician', on_delete=models.CASCADE)

    def __str__(self):
        return self.t_subject

class Technician(models.Model):
    te_name = models.CharField(max_length=150)
    te_id = models.CharField(max_length=100)
    te_phone = models.CharField(max_length=14)
    te_email = models.CharField(max_length=111)

    def __str__(self):
        return self.te_name
    
class Customer(models.Model):
    c_name = models.CharField(max_length=150)
    c_id = models.CharField(max_length=100)
    c_phone = models.CharField(max_length=14)
    c_email = models.CharField(max_length=111)

    def __str__(self):
        return self.c_name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
