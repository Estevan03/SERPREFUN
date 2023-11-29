from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .models import Product
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import TaskForm, CustomUserCreationForm, CustomAuthenticationForm, UserPermissionForm, ProductForm
from django.contrib.auth.models import User
from tasks.forms import CustomUserForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from .cart import Cart
from django.http import JsonResponse
from .forms import ServiceForm


# Vista para el registro
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"Usuario registrado: {user.username}, Rol: {user.role}")
            return redirect('tasks')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})




# Vista para el inicio de sesión
def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, 'Credenciales incorrectas. Por favor, verifica tu correo y contraseña.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'signin.html', {'form': form})

# Password reset views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    return render(request, 'home.html')

#about
def about(request):
    return render(request, 'about.html')

#productos
def product(request):
    return render(request, 'product.html')

#Servicios
def store(request):
    return render(request, 'store.html')

#Articulo destacado
def blog(request):
    return render(request, 'blog.html')

#Articulo destacado
def contact(request):
    return render(request, 'contact.html')

#Servicios Exequiales
def servicio1(request):
    return render(request, 'servicio1.html')

def servicio2(request):
    return render(request, 'servicio2.html')

def servicio3(request):
    return render(request, 'servicio3.html')

@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

#Vista para listar los usuarios en una plantilla del admin
@user_passes_test(lambda user: user.is_superuser and user.role == 'admin')
@login_required
def user_list(request):
    users = CustomUser.objects.all()

    # Verifica si el usuario actual tiene permisos de administrador
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a la lista de usuarios. Solicita permisos a otro administrador.')
        # Establece el mensaje de error antes de redirigir
        return redirect('home')  # Ajusta la redirección según tus necesidades

    users_with_permissions = []

    for user in users:
        permission_form = UserPermissionForm(initial={
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        })
        users_with_permissions.append({'user': user, 'form': permission_form})

    return render(request, 'user_list.html', {'users_with_permissions': users_with_permissions})



#Vista para activar y desactivar usuarios, ver perfil y editar usuarios
def activar_usuario(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_active = True
    user.save()
    return redirect('user_list')

def desactivar_usuario(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')

def ver_perfil(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'ver_perfil.html', {'user': user})

def editar_usuario(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirige de nuevo a la lista de usuarios después de guardar los cambios
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'editar_usuario.html', {'form': form, 'user': user})


#Vista para dar permisos a administradores
@user_passes_test(lambda user: user.is_superuser and user.role == 'admin')
@login_required
def manage_user_permissions(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    if request.method == 'POST':
        form = UserPermissionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permisos de usuario actualizados correctamente.')
            return redirect('user_list')
        else:
            messages.error(request, 'Error en el formulario. Por favor, verifica los datos ingresados.')
    else:
        form = UserPermissionForm(instance=user)

    return render(request, 'manage_user_permissions.html', {'form': form, 'user': user})


#Vista para html cliente_products.html
@login_required
def cliente_products(request):
    products = Product.objects.all()
    return render(request, 'cliente_products.html', {'products': products})


#Vista para html cliente_services.html

def cliente_services(request):
    # Lógica de la vista
    servicios = ["Producto 1", "Producto 2", "Producto 3"]  # Puedes obtener productos desde la base de datos u otro origen

    # Pasa los datos a la plantilla
    context = {'servicios': servicios}

    # Renderiza la plantilla
    return render(request, 'cliente_services.html', context)

#Vista empleado

@login_required
def empleado_home(request):
    # Lógica específica del empleado
    return render(request, 'empleado_home.html')


#Vista productos
def product_list(request):
    productos = Product.objects.all()
    return render(request, 'product_list.html', {'productos': productos})

def product_detail(request, product_id):
    # Lógica para obtener y mostrar los detalles del producto
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Guardar el producto en la base de datos
            product = form.save()

            # Obtener o crear el carrito para el usuario actual
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)

            # Crear o actualizar el CarritoItem
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            # Incrementar la cantidad en 1
            cart_item.quantity += 1
            cart_item.save()

            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve una respuesta JSON
                return JsonResponse({'success': True, 'message': 'Producto agregado al carrito exitosamente'})
            
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} se ha añadido al carrito.")
    return redirect('product_list')

#Vista carrito
@login_required
def shopping_cart(request):
    # Obtener el carrito para el usuario actual
    cart = ShoppingCart.objects.get(user=request.user)

    # Obtener los elementos del carrito
    cart_items = cart.cartitem_set.all()

    # Calcular el valor total para cada artículo
    for item in cart_items:
        item.total = item.quantity * item.product.price

    return render(request, 'shopping_cart.html', {'cart_items': cart_items})

#Vista eliminar 1 producto
def remove_one(request, product_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product__id=product_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    messages.success(request, 'Se eliminó 1 unidad del producto del carrito.')
    return redirect('shopping_cart')

#Vista eliminar todo el producto
def remove_all(request, product_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product__id=product_id)
    cart_item.delete()

    messages.success(request, 'Se eliminó todo el producto del carrito.')
    return redirect('shopping_cart')

#Vista agregar 1 producto
def add_one(request, product_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product__id=product_id)
    
    cart_item.quantity += 1
    cart_item.save()

    messages.success(request, 'Se agregó 1 unidad del producto al carrito.')
    return redirect('shopping_cart')


#Vista servicios
@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

@login_required
def add_service_to_cart(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)

    # Crear o actualizar el CarritoItem para el servicio
    cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service)

    # Incrementar la cantidad en 1
    cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({'success': True, 'message': 'Servicio agregado al carrito exitosamente.'})

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            # Guardar el servicio en la base de datos
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()

            return redirect('employee_service_list')  # Ajusta el nombre de la vista según tus URL
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})

def employee_service_list(request):
    # Obtener todos los servicios
    services = Service.objects.all()

    # Puedes agregar más lógica según tus necesidades
    
    return render(request, 'employee_service_list.html', {'services': services})