# from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .form import CreateUserForm, InsertProductForm, ProfileSendFrom
from .models import EstadoDespacho, Producto, Carro, CarroProducto, Perfil, Venta, Despacho
from django.db.models import Sum

# Create your views here.


def checkout(request):
    return render(request, 'core/checkout.html')


def cart(request):
    return render(request, 'core/cart.html')


def home(request):
    productos = Producto.objects.all()[:12]
    extra = {}
    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = User.objects.get(id=usuario_id)
        carrito = Carro.objects.get_or_create(user=usuario, activo=1)
        try:
            cantidad = CarroProducto.objects.filter(carro=carrito[0]).count()
            extra['cantidad'] = cantidad
        except:
            extra['cantidad'] = 0

    return render(request, 'core/home.html', {"productos": productos, "extra": extra})


def profile(request):
    extra = {}
    despacho = []
    lista_despacho = []

    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = User.objects.get(id=usuario_id)
        carrito = Carro.objects.get_or_create(user=usuario, activo=1)

        ventas = Venta.objects.filter(usuario=usuario)
        for i in ventas:
            lista_despacho.append(i.id)

        despacho = Despacho.objects.filter(venta__in=lista_despacho)

        if request.method == 'POST':
            form = ProfileSendFrom(request.POST)
            form.usuario = User.objects.get(id=usuario_id)
            if form.is_valid():
                form.save()

        try:
            cantidad = CarroProducto.objects.filter(carro=carrito[0]).count()
            extra['cantidad'] = cantidad
        except:
            extra['cantidad'] = 0

        try:

            try:
                Perfil.objects.get(usuario=usuario)
                return render(request, 'accounts/profile.html', {'extra': extra, 'form': form})

            except:
                return render(request, 'accounts/profile.html', {'extra': extra, 'ventas': ventas, 'despachos': despacho})

        except:
            form = ProfileSendFrom()

            return render(request, 'accounts/profile.html', {'extra': extra, 'form': form})
    return render(request, 'accounts/profile.html', {'extra': extra})


def signup(request):
    extra = {}
    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = User.objects.get(id=usuario_id)
        carrito = Carro.objects.get_or_create(user=usuario, activo=1)
        try:
            cantidad = CarroProducto.objects.filter(carro=carrito[0]).count()
            extra['cantidad'] = cantidad
        except:
            extra['cantidad'] = 0

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

    form = CreateUserForm()
    return render(request, 'accounts/signup.html', {'form': form, "extra": extra})


def products(request, id):
    form = InsertProductForm()
    extra = {}
    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = User.objects.get(id=usuario_id)
        carrito = Carro.objects.get_or_create(user=usuario, activo=1)
        try:
            cantidad = CarroProducto.objects.filter(carro=carrito[0]).count()
            extra['cantidad'] = cantidad
        except:
            extra['cantidad'] = 0

    if request.user.is_authenticated:
        if request.method == 'POST':
            gproducto = request.POST.get('producto')
            item = Producto.objects.get(id=gproducto)
            cantidad = int(request.POST.get('cantidad'))
            compra = request.POST.get('buy')
            precio = Producto.objects.filter(
                id=gproducto).values('precio')[0]['precio']

            try:
                CarroProducto.objects.get(
                    carro=carrito[0], producto=item)
                cantidad2 = CarroProducto.objects.values(
                    'cantidad').first()['cantidad']
                if cantidad2 != cantidad:

                    CarroProducto.objects.filter(
                        carro=carrito[0], producto=item).update(cantidad=cantidad, precio=(precio*cantidad))

            except:
                CarroProducto.objects.create(
                    carro=carrito[0], producto=item, cantidad=cantidad, precio=(precio*cantidad))

            if(compra != None):
                return redirect('buy')
            else:
                return redirect('home')
    producto = Producto.objects.get(id=id)

    return render(request, 'core/products.html', {'producto': producto, 'form': form, "extra": extra})


def buy(request):
    extra = {}

    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = User.objects.get(id=usuario_id)
        carrito = Carro.objects.get_or_create(user=usuario, activo=1)
        try:
            cantidad = CarroProducto.objects.filter(carro=carrito[0]).count()
            precio_total = CarroProducto.objects.filter(
                carro=carrito[0]).aggregate(Sum('precio'))
            extra['total'] = precio_total['precio__sum']
            extra['cantidad'] = cantidad
        except:
            extra['cantidad'] = 0

        items = CarroProducto.objects.filter(carro=carrito[0])

        return render(request, 'core/buy.html', {"extra": extra, 'productos': items})
    else:
        return redirect('signup')


def delete(request, id):
    producto = CarroProducto.objects.get(id=id)
    producto.delete()
    return redirect('buy')


def sell(request, discount):
    if request.user.is_authenticated:
        usuario_id = request.user.id
        usuario = User.objects.get(id=usuario_id)
        carro = Carro.objects.get(user_id=usuario_id, activo=1)

        for i in CarroProducto.objects.filter(carro=carro):

            producto = Producto.objects.get(
                id=i.producto_id)
            producto.stock = producto.stock - i.cantidad
            producto.save()

        carro.activo = 0
        carro.save()
        precio_total = CarroProducto.objects.filter(
            carro=carro).aggregate(Sum('precio'))

        if discount == 1:
            precio_total = precio_total-(precio_total * 5)/100

        venta = Venta(usuario=usuario,
                      monto=precio_total['precio__sum'], productos=carro, descuento=discount)
        venta.save()

        estado = EstadoDespacho.objects.get(nombre='Preparando')
        despacho = Despacho(origen='Local Principal',
                            ubicacion='Local Principal', venta=venta, estado=estado)
        despacho.save()

        return buy(request)
    else:
        return redirect('home')
