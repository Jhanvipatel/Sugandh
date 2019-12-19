# Create your models here.
from django.db import models


class brand(models.Model):
    brandID = models.CharField(max_length=8, primary_key=True)
    brandName = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class upscaledType(models.Model):
    upscaledTypeID = models.CharField(max_length=100, unique=True)
    upscaledName = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class fabric(models.Model):
    fabricID = models.CharField(primary_key=True, max_length=100)
    fabricName = models.CharField(max_length=100)
    fabricDesc = models.CharField(null=True, blank=True, max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class upscaledProduct(models.Model):
    serialNum = models.AutoField(primary_key=True)
    upscaledID = models.CharField(max_length=100, unique=True)
    upscaledName = models.CharField(max_length=100)
    upscaledDesc = models.CharField(null=True, blank=True, max_length=1000)
    up_productType = models.ForeignKey(upscaledType,on_delete=False)
    upscaledFabricType = models.ForeignKey(fabric,on_delete=False)
    upscaledProductPrice =models.PositiveIntegerField()
    upscaledProductQty = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class collection(models.Model):
    collectionID = models.CharField(primary_key=True, max_length=100)
    collectionName = models.CharField(max_length=100)
    collectionImage = models.CharField(max_length=200, blank=True, null=True)
    collectionDesc = models.CharField(null=True, blank=True, max_length=1000)
    brandID = models.ForeignKey(brand, on_delete=False)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = "sugandh_collection"


class category(models.Model):
    categoryID = models.CharField(primary_key=True, max_length=100)
    categoryName = models.CharField(max_length=100)
    categoryDesc = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class fit_type(models.Model):
    fitTypeID = models.CharField(primary_key=True, max_length=100)
    fitDes = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class size(models.Model):
    sizeID = models.CharField(primary_key=True, max_length=100)
    sizeDes = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class product_master(models.Model):
    serialNum = models.AutoField(primary_key=True)
    productID = models.CharField(max_length=100, unique=True)
    productName = models.CharField(max_length=100)
    productDesc = models.CharField(null=True, blank=True, max_length=1000)
    brandID = models.ForeignKey(brand, on_delete=False)
    collectionID = models.ForeignKey(collection, on_delete=False)
    categoryID = models.ForeignKey(category, on_delete=False)
    fabricID = models.ForeignKey(fabric, on_delete=False)
    fitType = models.ForeignKey(fit_type, on_delete=False)
    size = models.ForeignKey(size, on_delete=False)
    careInstructions = models.CharField(null=True, blank=True, max_length=1000)
    keywords = models.CharField(null=True, blank=True, max_length=1000)
    productState = models.BooleanField(default=True)
    productImage = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class product_price(models.Model):
    productID = models.ForeignKey(product_master, on_delete=False)
    originalPrice = models.PositiveIntegerField()
    discountRate = models.DecimalField(decimal_places=2, max_digits=5)
    discountPrice = models.DecimalField(decimal_places=2, max_digits=8)
    sellingPrice = models.DecimalField(decimal_places=3, max_digits=8)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class product_stock(models.Model):
    productID = models.ForeignKey(product_master, on_delete=False)
    productQty = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class customer_master(models.Model):
    customerID = models.CharField(primary_key=True, max_length=50)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    addLine1 = models.CharField(max_length=500)
    addLine2 = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.BigIntegerField()
    country = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    whatsappStatus = models.BooleanField(default=True)
    contactWhatsapp = models.CharField(max_length=50, blank=True, null=True)
    emailID = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    password = models.CharField(max_length=50)


class reseller_master(models.Model):
    resellerID = models.CharField(primary_key=True, max_length=50)
    logoURL = models.CharField(max_length=100)
    companyName = models.CharField(max_length=100)
    gst = models.CharField(max_length=50)
    resellerName = models.CharField(max_length=100)
    rAddLine1 = models.CharField(max_length=500)
    rAddLine2 = models.CharField(max_length=500, blank=True, null=True)
    rCity = models.CharField(max_length=50)
    rState = models.CharField(max_length=50)
    rZip = models.BigIntegerField()
    rCountry = models.CharField(max_length=50)
    addressStatus = models.BooleanField(default=True)
    oAddLine1 = models.CharField(max_length=500, blank=True, null=True)
    oAddLine2 = models.CharField(max_length=500, blank=True, null=True)
    oCity = models.CharField(max_length=50, blank=True, null=True)
    oState = models.CharField(max_length=50, blank=True, null=True)
    oZip = models.BigIntegerField(blank=True, null=True)
    oCountry = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50)
    whatsappStatus = models.BooleanField(default=True)
    contactWhatsapp = models.CharField(max_length=50, blank=True, null=True)
    emailID = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    bankName = models.CharField(max_length=200)
    account = models.CharField(max_length=100)
    codeIFSC = models.CharField(max_length=100)


