from charthandler.models.police import (
    PoliceCourtsAppealcases,
    PoliceCourtsFunctioning,
    PoliceCourtsJudgescases,
    PoliceCourtsOriginalcases,
    PoliceCyberCrimetypes,
    PoliceCyberFraudtypes,
    PoliceCyberTotals,
    PoliceDsaWomenchildrenTaluka,
    PoliceIpcDocpropertymarks,
    PoliceIpcHumanbody,
    PoliceIpcMisc,
    PoliceIpcProperty,
    PoliceIpcPublictranquility,
    PoliceIpcTotal,
    PolicePoliceEmployees,
    PolicePoliceInfrastructure,
    PoliceSllOffensetypes,
    PoliceSllTotal,
    PoliceWomenCrimetypes,
    PoliceWomenTotal
)

@admin.register(PoliceCourtsAppealcases)
class PoliceCourtsAppealcasesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCourtsAppealcases._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCourtsAppealcases._meta.fields] else []

@admin.register(PoliceCourtsFunctioning)
class PoliceCourtsFunctioningAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCourtsFunctioning._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCourtsFunctioning._meta.fields] else []

@admin.register(PoliceCourtsJudgescases)
class PoliceCourtsJudgescasesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCourtsJudgescases._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCourtsJudgescases._meta.fields] else []

@admin.register(PoliceCourtsOriginalcases)
class PoliceCourtsOriginalcasesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCourtsOriginalcases._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCourtsOriginalcases._meta.fields] else []

@admin.register(PoliceCyberCrimetypes)
class PoliceCyberCrimetypesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCyberCrimetypes._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCyberCrimetypes._meta.fields] else []

@admin.register(PoliceCyberFraudtypes)
class PoliceCyberFraudtypesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCyberFraudtypes._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCyberFraudtypes._meta.fields] else []

@admin.register(PoliceCyberTotals)
class PoliceCyberTotalsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceCyberTotals._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceCyberTotals._meta.fields] else []

@admin.register(PoliceDsaWomenchildrenTaluka)
class PoliceDsaWomenchildrenTalukaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceDsaWomenchildrenTaluka._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceDsaWomenchildrenTaluka._meta.fields] else []

@admin.register(PoliceIpcDocpropertymarks)
class PoliceIpcDocpropertymarksAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceIpcDocpropertymarks._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceIpcDocpropertymarks._meta.fields] else []

@admin.register(PoliceIpcHumanbody)
class PoliceIpcHumanbodyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceIpcHumanbody._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceIpcHumanbody._meta.fields] else []

@admin.register(PoliceIpcMisc)
class PoliceIpcMiscAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceIpcMisc._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceIpcMisc._meta.fields] else []

@admin.register(PoliceIpcProperty)
class PoliceIpcPropertyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceIpcProperty._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceIpcProperty._meta.fields] else []

@admin.register(PoliceIpcPublictranquility)
class PoliceIpcPublictranquilityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceIpcPublictranquility._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceIpcPublictranquility._meta.fields] else []

@admin.register(PoliceIpcTotal)
class PoliceIpcTotalAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceIpcTotal._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceIpcTotal._meta.fields] else []

@admin.register(PolicePoliceEmployees)
class PolicePoliceEmployeesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PolicePoliceEmployees._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PolicePoliceEmployees._meta.fields] else []

@admin.register(PolicePoliceInfrastructure)
class PolicePoliceInfrastructureAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PolicePoliceInfrastructure._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PolicePoliceInfrastructure._meta.fields] else []

@admin.register(PoliceSllOffensetypes)
class PoliceSllOffensetypesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceSllOffensetypes._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceSllOffensetypes._meta.fields] else []

@admin.register(PoliceSllTotal)
class PoliceSllTotalAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceSllTotal._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceSllTotal._meta.fields] else []

@admin.register(PoliceWomenCrimetypes)
class PoliceWomenCrimetypesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceWomenCrimetypes._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceWomenCrimetypes._meta.fields] else []

@admin.register(PoliceWomenTotal)
class PoliceWomenTotalAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PoliceWomenTotal._meta.fields]
    list_filter = ['year', 'district'] if 'year' in [f.name for f in PoliceWomenTotal._meta.fields] else []

