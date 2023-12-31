# Generated by Django 4.2.5 on 2023-10-18 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_graphic_link_alter_order_guest_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Initial deposit စောင့်ဆိုင်းနေသည်။', 'Initial deposit စောင့်ဆိုင်းနေသည်။'), ('Order မှာယူရန် စောင့်ဆိုင်းနေသည်။', 'Order မှာယူရန် စောင့်ဆိုင်းနေသည်။'), ('Order ရောက်ရှိရန် စောင့်ဆိုင်းနေသည်။', 'Order ရောက်ရှိရန် စောင့်ဆိုင်းနေသည်။'), ('Order ပေးပို့ရန် စောင့်ဆိုင်းနေသည်။', 'Order ပေးပို့ရန် စောင့်ဆိုင်းနေသည်။'), ('Order ပစ္စည်း delivery ကားပေါ်တွင်ရောက်ရှိပါပြီ။', 'Order ပစ္စည်း delivery ကားပေါ်တွင်ရောက်ရှိပါပြီ။')], default='Pending to confirm', max_length=100),
        ),
    ]
