from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cihaz
from .forms import CihazForm
import json
from django.utils import timezone

# Cihaz Listesi
def cihaz_list(request):
    cihazlar = Cihaz.objects.filter(visibility=True)

    # Çakışan cihazları belirleme
    conflicts = []
    cihaz_list_temp = list(cihazlar)
    for i, c1 in enumerate(cihaz_list_temp):
        for c2 in cihaz_list_temp[i+1:]:
            if (
                (c1.marka.lower(), c1.model.lower()) == (c2.marka.lower(), c2.model.lower())
                and (c1.destek_durumu.upper() != c2.destek_durumu.upper())
                and (c1.musteri == c2.musteri)
            ):
                if c1 not in conflicts:
                    conflicts.append(c1)
                if c2 not in conflicts:
                    conflicts.append(c2)

    has_conflicts = bool(conflicts)

    return render(request, 'cihazlar/cihaz_list.html', {
        'cihazlar': cihazlar,
        'conflicts': conflicts,
        'has_conflicts': has_conflicts,
    })

# Cihaz Silme
def cihaz_delete(request, id):
    if request.method == "POST":
        cihaz = get_object_or_404(Cihaz, id=id)
        cihaz.visibility = False
        cihaz.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Sadece POST destekleniyor."})

# Cihaz Ekleme
def cihaz_add(request):
    if request.method == "POST":
        form = CihazForm(request.POST)
        if form.is_valid():
            cihaz = form.save(commit=False)
            cihaz.kaynak_dosya = None
            cihaz.visibility = True
            cihaz.eklenme_tarihi = timezone.now().date()
            cihaz.save()
            return redirect('cihaz_list')
    else:
        form = CihazForm()
    return render(request, 'cihazlar/cihaz_form.html', {'form': form})

# Cihaz Düzenleme
def cihaz_edit(request, id):
    cihaz = get_object_or_404(Cihaz, id=id)
    if request.method == "POST":
        form = CihazForm(request.POST, instance=cihaz)
        if form.is_valid():
            cihaz = form.save(commit=False)
            cihaz.son_degistirilme = timezone.now()
            cihaz.save()
            return redirect('cihaz_list')
    else:
        form = CihazForm(instance=cihaz)
    return render(request, 'cihazlar/cihaz_form.html', {'form': form})

# AJAX ile Destek Durumu Güncelleme
def cihaz_update(request, id):
    if request.method == "POST":
        cihaz = get_object_or_404(Cihaz, id=id)
        try:
            data = json.loads(request.body)
            cihaz.destek_durumu = data.get("destek", cihaz.destek_durumu)
            cihaz.son_degistirilme = timezone.now()
            cihaz.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False}, status=400)

# AJAX ile CSV / Excel Upload
def cihaz_upload_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cihazlar = data.get("data", [])
            file_name = data.get("fileName", "CSV/Excel Upload")
            for row in cihazlar:
                Cihaz.objects.create(
                    marka=row.get('marka', ''),
                    model=row.get('model', ''),
                    destek_durumu=row.get('destek_durumu', ''),
                    aciklama=row.get('aciklama', ''),
                    musteri=row.get('musteri', ''),
                    test_durumu=row.get('test_durumu', ''),
                    # ✅ Yeni eklenen alanlar
                    platform=row.get('platform', ''),
                    note=row.get('note', ''),
                    supported_features=row.get('supported_features', ''),
                    model_note=row.get('model_note', ''),
                    kaynak_dosya=file_name,
                    visibility=True,
                    eklenme_tarihi=timezone.now().date()
                )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Sadece POST destekleniyor."})
