import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from auction.models import Product, Bid

''''''
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from auction.models import Product, Bid



@login_required(login_url='authentication:user-login')
def auction_gallery(request):
    
    # List of all the auction items
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    context = {'products': products, 'active': 'auction_gallery'}
    return render(request, 'auction_gallery.html', context)


@login_required(login_url='authentication:user-login')
def item_details(request, slug):

    #Auction item detail info
    selected_product = get_object_or_404(Product, slug=slug)
    selected_products_bids = Bid.objects.filter( product=selected_product).order_by('-price')

    context = {
        'selected_product': selected_product,
        'bids': selected_products_bids,
    }
    return render(request, 'detail.html', context)


@login_required(login_url='authentication:user-login')
def create_auction(request):

    # Create a new auction for a product.
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_photo = request.FILES.get('product_photo')
        min_bid_price = request.POST.get('min_bid_price')
        auction_end_date = request.POST.get('auction_end_date')
        auction_end_time = request.POST.get('auction_end_time')

        context = {
            'product_name': product_name,
            'product_description': product_description,
            'min_bid_price': min_bid_price,
            'auction_end_date': auction_end_date,
            'auction_end_time': auction_end_time
        }
        create_auction_template = 'create_auction.html'

        if product_name.strip() == '':
            messages.error(request, 'Please give a product name!')
            return render(request, create_auction_template, context)
        if product_description.strip() == '':
            messages.error(request,'Please write some description about the product!')
            return render(request, create_auction_template, context)
        if product_photo == '':
            messages.error(request, 'Please add a photo of the product!')
            return render(request, create_auction_template, context)
        if min_bid_price == '':
            messages.error(request, 'Please give minimum bid price!')
            return render(request, create_auction_template, context)
        if auction_end_date == '':
            messages.error(request, 'Please give auction end date!')
            return render(request, create_auction_template, context)
        if auction_end_time == '':
            messages.error(request, 'Please give auction end time!')
            return render(request, create_auction_template, context)
        else:
            try:
                # format the auction_end_date with date time
                auction_end_date_time = datetime.datetime.strptime(
                    f"{auction_end_date} {auction_end_time}",
                    "%Y-%m-%d %H:%M"
                )
                timezone_aware_auction_end_datetime = timezone.make_aware(
                    auction_end_date_time,
                    timezone.get_current_timezone()
                )
                # Create a new product object
                Product.objects.create(
                    name=product_name,
                    description=product_description,
                    photo=product_photo,
                    min_bid_price=min_bid_price,
                    auction_end_date=timezone_aware_auction_end_datetime,
                    user=request.user,
                )
                return redirect('auction:dashboard')
            except Exception as e:
                # print(e)
                messages.error(request, f"Error: {e}")
                redirect('auction:create-auction')

    return render(request, 'create_auction.html')


@login_required(login_url='authentication:user-login')
def my_auctions(request):

    #List of the auction of single user.

    products = Product.objects.filter(user=request.user, is_active=True)
    context = {
        'products': products,
        'active': 'my_auctions'
    }
    return render(request, 'auction_gallery.html', context)


@login_required(login_url='authentication:user-login')
def place_bid(request, slug):

    # Place bid for selected auction product/item.
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        bid_price = request.POST.get('bid_price')

        # Validating bid value
        if not isinstance(int(bid_price), int):
            messages.error(request, 'Please place correct bid.')
            return redirect(product)
        try:
            Bid.objects.create(
                product=product,
                bidder=request.user,
                price=bid_price
            )
            return redirect(product)
        except Exception as e:
            # print(e)
            messages.error(request, f'Error: {e}')
            return redirect(product)
    return redirect(product)


@login_required(login_url='authentication:user-login')
def update_bid(request, slug, hashed_id):

    # Update the bid
    product = get_object_or_404(Product, slug=slug)
    bid = get_object_or_404(Bid, hashed_id=hashed_id)

    if request.method == "POST":
        updated_bid_price = request.POST.get("updated_bid_price")
        try:
            bid.price = updated_bid_price
            bid.save()

            return redirect('auction:item-detail', slug=slug)
        except Exception as e:
            # print(e)
            messages.error(request, f'Error: {e}')
            return redirect(product)

    return redirect(product)

'''' '''
''''''
''''''

@login_required(login_url='authentication:user-login')
def dashboard(request):
    """
    User and Admin Dashboard
    """
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    total_auctions = products.count()
    running_auctions_count = 0
    running_auctions_total_value = 0
    if products.count() > 0:
        # ***Running Auctions
        running_auctions = products.filter(
            auction_end_date__gt=datetime.datetime.now(
                products.first().auction_end_date.tzinfo
            )
        )
        running_auctions_count = running_auctions.count()

        # ***Running Auction's total value
        for product in running_auctions:
            max_bid_price_for_product = Bid.objects.filter(
                product=product
            ).order_by('-price').first()  # Max bid

            if max_bid_price_for_product is None:  # If no bid for the auction
                running_auctions_total_value += product.min_bid_price
            else:
                running_auctions_total_value += max_bid_price_for_product.price

    context = {
        'products': products,
        'active': 'dashboard',
        'running_auctions_count': running_auctions_count,
        'total_auctions': total_auctions,
        'running_auctions_total_value': int(running_auctions_total_value),
    }

    return render(request, 'dashboard.html', context)


