# charthandler/models/__init__.py
# Re-export all models so existing imports (e.g. from charthandler.models import X) keep working.

from .chart_template import ChartTemplate

from .livestock import (
    LivestockNumbers,
    ArtificialInsemination,
    DairyCooperative,
    DairyByproduct,
    Fisheries,
    Veterinary,
)

from .agriculture import (
    AgcGrosscroppedarea,
    AgcHoldingsarea,
    AgcHoldingsnumber,
    AgcLanduse,
    DsaChemicalfertilizer,
    DsaIrrigationbeneficiary,
    DsaIrrigationfacilities,
    DsaIrrigationprojects,
    DsaIrrigationwells,
    DsaTubewellshandpumps,
)

from .health import (
    # DSA
    DSAFamilyWelfarePrograms,
    DSAVaccines,
    DSAMalnutrition,
    DSAMalnutrition2,
    DSARegisteredBirths,
    DSAReportedDeaths,
    DSADeathCause,
    DSAPublicHospitals2,
    DSAPrivateHealth2,
    DSAAnganwadis,
    DSAPublicOutPatients,
    # HMIS
    HMISFamilyPlanning,
    HMISContraceptives,
    HMISInfantVaccinations,
    HMISIV2,
    HMISIV,
    HMISAnaemia,
    HMISAntenatalCare,
    HMISDeliveries,
    HMISMDeaths,
    HMISCSection,
    HMISSexRatio,
    HMISAbortion,
    HMISInfantDeaths2,
    HMISInfantDeaths,
    HMISChildDisease2,
    HMISChildDisease,
    HMISPatients,
    # NFHS
    NFHSFamilyPlanning,
    NFHSVaccinations,
    NFHSOverweight,
    NFHSMalnutrition,
    NFHSLowBMI,
    NFHSAnaemia,
    NFHSDeliveryExpenditure,
    NFHSIFAConsumption,
    NFHSPostnatalCare,
    NFHSSexRatio,
    NFHSBirths,
    NFHSCSection,
    NFHSDiet,
    NFHSHighBloodSugar,
    NFHSCancerScreening2,
    NFHSCancerScreening,
    NFHSHypertension,
    NFHSTobaccoAlcohol,
    NFHSFacilities,
)

from .industry import (
    ECNumber,
    ECSocialGroup,
    ECSourcesOfFinance,
    ECSourcesOfBorrowings,
    ECType,
    ECBroadActivity,
    DSAMsme,
    FactoryWorkers,
    DSAElectricity,
    DSAPollutionCategory,
)

from .labor import (
    LaborWorkers,
    LaborAgeDistribution,
    LaborECWorkers,
    LaborECGender,
    LaborECReligion,
    LaborMNREGAJobCards,
    LaborMNREGAParticipation,
    LaborMNREGAAccounts,
    LaborMNREGAScope,
    LaborGovtEmployees,
    LaborDSAEstablishments,
    LaborDSAWorkers,
    LaborIndustryType,
)

from .demography import (
    CensusPopulation,
    CensusSC,
    CensusST,
    CensusAgeDistribution,
    CensusLiterate,
    CensusWorking,
    CensusInwardMigrationA,
    CensusInwardMigrationB,
    CensusInwardMigrationC,
    CensusInwardMigrationD,
    CensusInwardMigrationE,
    CensusMotherTongue,
    CensusReligion,
    CensusSexRatio,
    CensusToiletFacility,
    CensusCooking,
    CensusWater,
    CensusElectricity,
    CensusTCAssets,
    CensusOwnership,
)

from .transport import (
    TransportARCAccidents,
    TransportARCAge,
    TransportARCCaseFine,
    TransportARCFatalities,
    TransportARCGrievousInjuries,
    TransportARCInjuries,
    TransportARCMinorInjuries,
    TransportARCModeTransport,
    TransportARCMonth,
    TransportARCRoadType,
    TransportARCTime,
    TransportARCTotalsInjuryDeath,
    TransportDSA100sqkm,
    TransportDSABus,
    TransportDSAMagazine,
    TransportDSARoadMaterial,
    TransportDSARoadType,
    TransportTCAssets,
)

from .revenue import *

from .police import *

from .education import (
    DropOutRateByGender,
    DropOutRateSchoolingStage,
    EducationLevels,
    NoOfSchools,
    NoOfSchoolsManagementType,
    NoOfSchoolsType,
    NoOfTeachersByType,
    StudentEnrollmentBoysVsGirls,
    StudentEnrollmentClassWise,
    StudentEnrollmentGirlsVsBoys,
    StudentEnrollmentNumbers,
    TeacherCategory,
    TeacherSocialCategory,
)

from .environment import (
    EnvWildlifeProjects,
    EnvForestArea,
    EnvForestDensity,
    EnvNightLightIntensity,
    EnvRunoff,
    EnvRainyDays,
    EnvRainfall,
    EnvMinTemperature,
    EnvMaxTemperature,
    EnvWindSpeed,
    EnvWaterDeficit,
    EnvHumidity,
    EnvSoilMoisture,
    EnvEvapotranspirationYearly,
    EnvEvapotranspirationMonthly,
    EnvBorewells,
    EnvDugwells,
)
