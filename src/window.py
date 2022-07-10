# window.py
#
# Copyright 2022 Muhammad Rivan
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

import webbrowser
from gi.repository import Gtk, GLib
from currency_converter import CurrencyConverter
from threading import Thread
from . import stringbuddy as sb
from . import gousername as gu

@Gtk.Template(resource_path='/org/example/App/window.ui')
class StringbuddydemoWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'StringbuddydemoWindow'

    cc = None
    ent_keyword = Gtk.Template.Child()
    sw_whatisthis = Gtk.Template.Child()
    vp_whatisthis = Gtk.Template.Child()

    lbl_c_uname_result = Gtk.Template.Child()
    lbl_c_currency_result = Gtk.Template.Child()
    lbl_result = Gtk.Template.Child()
    
    rvl_open_browser = Gtk.Template.Child()
    rvl_chat_telegram = Gtk.Template.Child()
    rvl_chat_whatsapp = Gtk.Template.Child()
    rvl_check_username = Gtk.Template.Child()
    rvl_convert_currency = Gtk.Template.Child()
    rvl_c_currency_result = Gtk.Template.Child()
    rvl_c_uname_result = Gtk.Template.Child()
    rvl_result = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def present(self, **kwargs):
        super().present(**kwargs)

    @Gtk.Template.Callback()
    def on_ent_keyword_search_changed(self, widget):
        text = widget.get_text()
        show_result = False
        show_open_browser = False
        show_check_username = False
        show_chat_telegram = False
        show_chat_whatsapp = False
        show_convert_currency = False

        if text:
            result = sb.get_type(text)
            show_result = True

            if result == sb.unknown:
                self.lbl_result.set_label(f"Saya tidak tahu ini apa...")
            else:
                self.lbl_result.set_label(f"Ini {result.to_string()}...")

            if result == sb.url:
                show_open_browser = True
            elif result == sb.username:
                show_check_username = True
            elif result == sb.usernameUrl:
                show_open_browser = True
                show_check_username = True
            elif result == sb.phonenumber:
                if text[0] == '+':
                    show_chat_telegram = True
                    
                show_chat_whatsapp = True
            elif result == sb.currency:
                show_convert_currency = True
            
        self.rvl_result.set_reveal_child(show_result)
        self.rvl_open_browser.set_reveal_child(show_open_browser)
        self.rvl_chat_telegram.set_reveal_child(show_chat_telegram)
        self.rvl_chat_whatsapp.set_reveal_child(show_chat_whatsapp)
        
        self.rvl_convert_currency.set_reveal_child(show_convert_currency)
        self.rvl_c_currency_result.set_reveal_child(False)
        
        self.rvl_check_username.set_reveal_child(show_check_username)
        self.rvl_c_uname_result.set_reveal_child(False)

    @Gtk.Template.Callback()
    def on_btn_open_browser_clicked(self, widget):
        url = self.ent_keyword.get_text()

        if ':' in url:
            webbrowser.open(url)
        else:
            webbrowser.open(f"http://{url}")

    def scroll_to_bottom(self, smooth=False):
        va = self.sw_whatisthis.get_vadjustment()
        anim = 500
        step = 25 if smooth else 250

        for i in range(step, anim, step):
            GLib.timeout_add(i, va.set_value, va.get_upper() * 2)

    def check_username_and_append(self, ison):
        username = self.ent_keyword.get_text()
        new_text = ison(username).to_string()

        GLib.idle_add(
            self.lbl_c_uname_result.set_label,
            f"{self.lbl_c_uname_result.get_label()}\n{new_text}"
        )
        self.scroll_to_bottom()

    @Gtk.Template.Callback()
    def on_btn_check_username_clicked(self, widget):
        isons = [
            gu.is_on_github, gu.is_on_gitlab, gu.is_on_facebook,
            gu.is_on_dribbble, gu.is_on_deviantart, gu.is_on_bitbucket,
            gu.is_on_medium, gu.is_on_youtube, gu.is_on_askfm
        ]

        self.rvl_c_uname_result.set_reveal_child(True)
        self.lbl_c_uname_result.set_label('')

        for i in isons:
            Thread(target=self.check_username_and_append, args=[i]).start()

    @Gtk.Template.Callback()
    def on_btn_chat_telegram_clicked(self, widget):
        phonenumber = self.ent_keyword.get_text()
        webbrowser.open(f"https://t.me/{sb.get_number_only(phonenumber)}")
        
    @Gtk.Template.Callback()
    def on_btn_chat_whatsapp_clicked(self, widget):
        phonenumber = self.ent_keyword.get_text()
        webbrowser.open(f"https://wa.me/{sb.get_number_only(phonenumber)}")
        
    @Gtk.Template.Callback()
    def on_btn_convert_currency_clicked(self, widget):
        rawtext = self.ent_keyword.get_text()
        currency = sb.get_currency(rawtext)
        money = sb.parse_number(rawtext)
        result = ''
        
        if not self.cc:
            self.cc = CurrencyConverter(fallback_on_missing_rate=True)
        
        self.rvl_c_currency_result.set_reveal_child(True)
        self.lbl_c_currency_result.set_label(
            f'{money} {currency} setara dengan...\n'
        )
        
        for i in self.cc.currencies:
            try:
                money_result = self.cc.convert(float(money), currency, i)
                result += f'\n{i}: {round(money_result, 2)}'
            except:
                result += f'\n{i}: -'

        self.lbl_c_currency_result.set_label(
            f'{self.lbl_c_currency_result.get_label()}{result}'
        )
        self.scroll_to_bottom(True)