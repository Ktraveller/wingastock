import polib

po_file = "locale/sw/LC_MESSAGES/django.po"
mo_file = "locale/sw/LC_MESSAGES/django.mo"

po = polib.pofile(po_file)
po.save_as_mofile(mo_file)

print("Translation compiled successfully!")