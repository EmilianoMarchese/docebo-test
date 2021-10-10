CREATE DATABASE `docebo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
DROP TABLE IF EXISTS `AirQuality`;
CREATE TABLE `AirQuality`
(
    MeasureId           int null,
    MeasureName         text null,
    MeasureType         text null,
    StratificationLevel text null,
    StateFips           int null,
    StateName           text null,
    CountyFips          int null,
    CountyName          text null,
    ReportYear          int null,
    Value               float null,
    Unit                text null,
    UnitName            text null,
    DataOrigin          text null,
    MonitorOnly         int null
);
