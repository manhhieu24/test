from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import  CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from app.comment.models import CommentModel
from .comment.forms import CommentForm
from .models import CartItemModel, ProductModel, CategoryModel
from .forms import ProductForm, RegistrationForm, UserEditForm, SearchForm
from django.contrib import messages
from django.db.models import Avg, Count





class ProductCreateView(CreateView):
    model = ProductModel
    form_class = ProductForm
    template_name = 'app/create_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner_shop = self.request.user
        return super().form_valid(form)



class ProductListView():
    def product_list(request):
        products = ProductModel().get_product_all()
        categories = CategoryModel().get_category_all()
        context = {'products':products, 'categories':categories}
        return render(request, 'app/product_list.html', context)
    


class CategoryView():  
    def category(request, pk):
        category = CategoryModel().get_category(pk)
        products = category.products.all()
        return render(request, 'app/product_list.html', {'products': products})



class ProductDetailView():
    def product_detail(request, pk):
        product = ProductModel().get_product(pk)
        related_products = product.get_related_products()
        comments = CommentModel.objects.filter(product=product)

        average_stars = comments.aggregate(Avg('stars'))['stars__avg']
        star_counts = comments.values('stars').annotate(count=Count('stars'))
        star_count_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for star_count in star_counts:
            star_count_dict[star_count['stars']] = star_count['count']

        total_comments = comments.count()
        star_percentage = {star: (count / total_comments) * 100 if total_comments > 0 else 0
                           for star, count in star_count_dict.items()}
        cart = None
        form = None

        if request.user.is_authenticated:
            cart = CartItemModel.objects.filter(customer=request.user, product=product).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = CartItemModel.objects.filter(session_key=session_key, product=product).first()

        if request.method == 'POST':
            if 'add_to_cart' in request.POST:
                cart = cart or CartItemModel(
                    customer=request.user if request.user.is_authenticated else None,
                    session_key=session_key if not request.user.is_authenticated else None,
                    product=product,
                    quantity=0
                )
                cart.quantity += 1
                cart.save()
                return HttpResponseRedirect(request.path_info)

            if 'add_comment' in request.POST and request.user.is_authenticated:
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.product = product
                    comment.customer = request.user
                    comment.save()
                    return redirect('product_detail', pk=pk)
            else:
                form = CommentForm()

        else:
            if request.user.is_authenticated:
                form = CommentForm()

        context = {
            'cart': cart,
            'product': product,
            'form': form,
            'comments': comments,
            'average_stars': average_stars,
            'star_count_dict': star_count_dict,
            'star_percentage': star_percentage,
            'total_comments':  total_comments,
            'related_products': related_products
        }
        return render(request, 'app/product_detail.html', context)



class CartView():
    def cart_view(request, pk):
        cart = CartItemModel().get_cart_item(pk)
        context = {'cart': cart}
        return render(request, 'app/cart_views.html', context)



class CheckoutView: 
    def check_out(request, pk):
        cart_items = CartItemModel().get_cart_item(pk)
        cart_total = CartItemModel().get_total_cart_items(pk)[0]
        
        context = {'total_sum_price': cart_total, 'cart_item':cart_items}
        return render(request, 'app/checkout.html', context)



class RegistrationView(FormView):
    template_name = 'app/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('product_list') 

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('product_list')  



class DeleteProductView():
    def delete_product_from_model(request, pk):
        if request.method == 'POST':
            CartItemModel().delete_product(pk)
            current_url = reverse('product_list') 
            return HttpResponseRedirect(current_url)



class EditAccountView():
    def edit_account(request):
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been updated successfully.')
                return redirect('product_list')
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'app/edit_account.html', {'form': form})
    


class EditProductView():
    def edit_product(request, pk):
        product = ProductModel().get_product(pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_detail', pk=product.pk)
        else:
            form = ProductForm(instance=product)
        return render(request, 'app/edit_product.html', {'form': form, 'product': product})



class SearchProductView:
    @staticmethod
    def search_view(request):
        form = SearchForm()
        results = []
        query = ""
        
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                results = ProductModel.objects.filter(name__icontains=query)

        context = {
            'results': results,
            'query': query,
        }
        return render(request, 'app/base.html', context)


