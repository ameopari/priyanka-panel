from django.contrib import admin
from Employee.models import ForgetPassword, Product, Student, Page, Parent, Child, UserProfile
# Register your models here.

admin .site.register(Student)
admin .site.register(ForgetPassword)
admin .site.register(Product)
admin.site.register(Page)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(UserProfile)