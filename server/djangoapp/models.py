from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    Name = models.CharField(null=False, 
    max_length=20)
    Description = models.TextField()

    def __str__(self):
        return self.Name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, 
# using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices 
#   such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    Make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Name = models.CharField(null=False, max_length=10)
    SUV = 'SUV'
    SEDAN = 'Sedan'
    SPORTS_CAR   = 'Sports Car'
    XOVER = 'Crossover'
    TYPE_CHOICES = [
        (SUV, 'SUV'),
        (SEDAN, 'Sedan'),
        (SPORTS_CAR, 'Sports Car'),
        (XOVER, 'Crossover'),
    ]
    Type = models.CharField(
        null=False,
        max_length=10,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    Year = models.DateField(null=False)

    def __str__(self):
        return f"{self.Year.year} {self.Make.__str__()} {self.Name} ({self.Type})" 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer: 
    def __init__(self, id, city, state, st, address, zip, latitude, longitude, short_name, full_name):
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.latitude = latitude
        self.longitude = longitude
        self.short_name = short_name
        self.full_name = full_name
    
    def __str__(self):
        return f"Dealer: {self.full_name}"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.id = id
        self.name = name,
        self.dealership=  dealership
        self.review = review
        self.purchase = purchase 
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    def __str__(self):
        return f"Review: {self.review}"

