from django.db import models

# Create your models here.

class FacultyLogin(models.Model):
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email
    class Meta:
        db_table = "FacultyLogin"
        
    
class FacultyProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('Maths', 'Mathematics & Computing'),
        ('PH', 'Physics'),
        ('CH', 'Chemistry'),
        ('CE', 'Civil Engineering'),
        # Add more departments if needed
    ]

    login = models.OneToOneField(FacultyLogin, on_delete=models.CASCADE, related_name='profile')

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    office_number = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='faculty_photos/', blank=True, null=True)

    about_me = models.TextField(blank=True, null=True)
    research_interest = models.TextField(blank=True, null=True)

    cv_upload = models.FileField(upload_to='faculty_cvs/', blank=True, null=True)
    publications_upload = models.FileField(upload_to='faculty_publications/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "FacultyProfile"
    
class Teaching(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='teachings')
    teaching_description = models.TextField()


    def __str__(self):
        return f"{self.teaching_description} ({self.faculty})"

    class Meta:
        db_table = "Teaching"
    

    
    
class Academics(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='academics')
    academics_description = models.TextField()
   

    def __str__(self):
        return f"{self.academics_description} "

    class Meta:
        db_table = "Academics"
        
class Positions(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='positions')
    roles = models.TextField()
    
    def __str__(self):
        return f"{self.roles} "

    class Meta:
        db_table = "Positions"
        
class AwardHonor(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='awards')
    name = models.TextField(verbose_name="Name of the Award")
   

    def __str__(self):
        return f"{self.name} "

    class Meta:
        db_table = "AwardHonor"
        
class Publication(models.Model):


    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='publications')
    publications = models.TextField()

    def __str__(self):
        return self.publications

    class Meta:
        db_table = "Publication"
    
class Project(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='projects')
    project_description = models.TextField()
    
    def __str__(self):
        return self.project_description

    class Meta:
        db_table = "Project"
    
    
class Guidance(models.Model):


    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='guidances')

    guidance_details = models.TextField()
    

    def __str__(self):
        return f"{self.guidance_details} "

    class Meta:
        db_table = "Guidance"




