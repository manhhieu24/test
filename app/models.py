from django.db import connection, models
from django.contrib.auth.models import User



class CategoryModel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_category_all(self):
        raw_query_category = 'SELECT * FROM app_categorymodel'
        category = CategoryModel.objects.raw(raw_query_category)
        return category

    def get_category(self, id):
        raw_query_category = 'SELECT * FROM app_categorymodel WHERE id = %s'
        category = CategoryModel.objects.raw(raw_query_category, [id])[0]
        return category

class ProductModel(models.Model):
    owner_shop = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to= 'products/', blank=True, null=True)

    def __str__(self):
        return self.name
        
    def get_product_all(self):
        raw_query_product = 'SELECT * FROM app_productmodel ORDER BY id DESC'
        product = ProductModel.objects.raw(raw_query_product)
        return product
    
    def get_product(self, id):
        raw_query_product = 'SELECT * FROM app_productmodel WHERE id = %s'
        product = ProductModel.objects.raw(raw_query_product, [id])[0]
        return product
    
    def get_related_products(self):
        return ProductModel.objects.filter(category=self.category).exclude(id=self.id)[:4]



class CartItemModel(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40, null=True, blank=True)
   
    def __str__(self):
        return f'{self.product.name} {self.quantity}'

    def get_cart_item_from_user(self, customer_id) :
        raw_query_cart = 'SELECT id, product_id, user_id, quantity FROM app_cartitemmodel WHERE customer_id = %s'
        quantity = CartItemModel.objects.raw(raw_query_cart, [customer_id])
        return quantity

    def get_cart_item(self, customer_id):
        raw_query_cart_user = 'SELECT c.id, p.name, c.quantity, p.price, (p.price * c.quantity) AS total_price FROM app_cartitemmodel AS c INNER JOIN app_productmodel AS p ON c.product_id = p.id WHERE c.customer_id = %s'
        return  CartItemModel.objects.raw(raw_query_cart_user, [customer_id])
    
    def get_total_cart_items(self, customer_id):
        with connection.cursor() as cursor:
            raw_query_sum ='SELECT SUM(p.price * c.quantity) AS total_price FROM app_cartitemmodel c INNER JOIN app_productmodel p ON c.product_id = p.id WHERE c.customer_id = %s'
            cursor.execute(raw_query_sum, [customer_id])
            return cursor.fetchone()

    def delete_product(self, product_id):
        raw_query_delete = 'DELETE FROM app_cartitemmodel WHERE product_id = %s'
        with connection.cursor() as cursor:
            cursor.execute(raw_query_delete, [product_id])
            return cursor.fetchone()



