from django.db import models

# Create your models here.

class GlobalContact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    spam_points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name+' '+self.phone_number

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__startswith=query).order_by('name') | \
               cls.objects.filter(name__icontains=query).exclude(name__startswith=query).order_by('name')

    @classmethod
    def search_by_phone_number(cls, query):
        return cls.objects.filter(phone_number=query)
    
    @classmethod
    def add_phone_number(cls, name, phone_number):
        global_contact, created = cls.objects.get_or_create(phone_number=phone_number)
        if created:
            global_contact.phone_number = phone_number
            global_contact.name = name
            global_contact.save()
    

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username+' '+self.phone_number
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        GlobalContact.add_phone_number(self.username, self.phone_number)

    def mark_contact_as_spam(self, contact):
        if not contact.is_spam:
            contact.is_spam = True
            contact.save()
            global_contact = GlobalContact.objects.get(phone_number=contact.phone_number)
            global_contact.spam_points += 1
            global_contact.save()
            
    def add_contacts(self, contacts):
        for contact_data in contacts:
            contact = Contact.objects.create(user=self, **contact_data)
            # GlobalContact.add_phone_number(contact.name, contact.phone_number)

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_spam = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name+' '+self.phone_number

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
        GlobalContact.add_phone_number(self.name, self.phone_number)




# class GlobalContact(models.Model):
#     name = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=15)
#     spam_points = models.IntegerField(default=0)

# class User(models.Model):
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     password = models.CharField(max_length=255)
    
# class Contact(models.Model):
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15)
#     is_spam = models.BooleanField()
   