#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
from typing import Any
from pysnmp.entity.engine import SnmpEngine
from pysnmp.error import PySnmpError
from pysnmp.smi.error import SmiError, NoSuchInstanceError
from pysnmp.entity import config


def getTargetAddr(snmpEngine: SnmpEngine, snmpTargetAddrName):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    (snmpTargetAddrEntry,) = mibBuilder.importSymbols(  # type: ignore
        "SNMP-TARGET-MIB", "snmpTargetAddrEntry"
    )

    cache: "dict[str, Any] | None" = snmpEngine.getUserContext("getTargetAddr")
    if cache is None:
        cache = {"id": -1}
        snmpEngine.setUserContext(getTargetAddr=cache)

    if cache["id"] != snmpTargetAddrEntry.branchVersionId:
        cache["nameToTargetMap"] = {}

    nameToTargetMap = cache["nameToTargetMap"]

    if snmpTargetAddrName not in nameToTargetMap:
        (
            snmpTargetAddrTDomain,
            snmpTargetAddrTAddress,
            snmpTargetAddrTimeout,
            snmpTargetAddrRetryCount,
            snmpTargetAddrParams,
        ) = mibBuilder.importSymbols(  # type: ignore
            "SNMP-TARGET-MIB",
            "snmpTargetAddrTDomain",
            "snmpTargetAddrTAddress",
            "snmpTargetAddrTimeout",
            "snmpTargetAddrRetryCount",
            "snmpTargetAddrParams",
        )
        (snmpSourceAddrTAddress,) = mibBuilder.importSymbols("PYSNMP-SOURCE-MIB", "snmpSourceAddrTAddress")  # type: ignore

        tblIdx = snmpTargetAddrEntry.getInstIdFromIndices(snmpTargetAddrName)

        try:
            snmpTargetAddrTDomain = snmpTargetAddrTDomain.getNode(
                snmpTargetAddrTDomain.name + tblIdx
            ).syntax
            snmpTargetAddrTAddress = snmpTargetAddrTAddress.getNode(
                snmpTargetAddrTAddress.name + tblIdx
            ).syntax
            snmpTargetAddrTimeout = snmpTargetAddrTimeout.getNode(
                snmpTargetAddrTimeout.name + tblIdx
            ).syntax
            snmpTargetAddrRetryCount = snmpTargetAddrRetryCount.getNode(
                snmpTargetAddrRetryCount.name + tblIdx
            ).syntax
            snmpTargetAddrParams = snmpTargetAddrParams.getNode(
                snmpTargetAddrParams.name + tblIdx
            ).syntax
            snmpSourceAddrTAddress = snmpSourceAddrTAddress.getNode(
                snmpSourceAddrTAddress.name + tblIdx
            ).syntax
        except NoSuchInstanceError:
            raise SmiError("Target %s not configured to LCD" % snmpTargetAddrName)

        if snmpEngine.transportDispatcher is None:
            raise PySnmpError("TransportDispatcher not set")
        transport = snmpEngine.transportDispatcher.getTransport(snmpTargetAddrTDomain)

        if snmpTargetAddrTDomain[: len(config.snmpUDPDomain)] == config.snmpUDPDomain:
            (
                SnmpUDPAddress,
            ) = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols(  # type: ignore
                "SNMPv2-TM", "SnmpUDPAddress"
            )
            addr = transport.addressType(  # type: ignore
                SnmpUDPAddress(snmpTargetAddrTAddress)
            ).setLocalAddress(SnmpUDPAddress(snmpSourceAddrTAddress))
        elif (
            snmpTargetAddrTDomain[: len(config.snmpUDP6Domain)] == config.snmpUDP6Domain
        ):
            (TransportAddressIPv6,) = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols(  # type: ignore
                "TRANSPORT-ADDRESS-MIB", "TransportAddressIPv6"
            )
            addr = transport.addressType(  # type: ignore
                TransportAddressIPv6(snmpTargetAddrTAddress)
            ).setLocalAddress(TransportAddressIPv6(snmpSourceAddrTAddress))
        elif (
            snmpTargetAddrTDomain[: len(config.snmpLocalDomain)]
            == config.snmpLocalDomain
        ):
            addr = transport.addressType(snmpTargetAddrTAddress)  # type: ignore

        nameToTargetMap[snmpTargetAddrName] = (
            snmpTargetAddrTDomain,
            addr,
            snmpTargetAddrTimeout,
            snmpTargetAddrRetryCount,
            snmpTargetAddrParams,
        )

        cache["id"] = snmpTargetAddrEntry.branchVersionId

    return nameToTargetMap[snmpTargetAddrName]


def getTargetParams(snmpEngine: SnmpEngine, paramsName):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    (snmpTargetParamsEntry,) = mibBuilder.importSymbols(  # type: ignore
        "SNMP-TARGET-MIB", "snmpTargetParamsEntry"
    )

    cache: "dict[str, Any] | None" = snmpEngine.getUserContext("getTargetParams")
    if cache is None:
        cache = {"id": -1}
        snmpEngine.setUserContext(getTargetParams=cache)

    if cache["id"] != snmpTargetParamsEntry.branchVersionId:
        cache["nameToParamsMap"] = {}

    nameToParamsMap = cache["nameToParamsMap"]

    if paramsName not in nameToParamsMap:
        (
            snmpTargetParamsMPModel,
            snmpTargetParamsSecurityModel,
            snmpTargetParamsSecurityName,
            snmpTargetParamsSecurityLevel,
        ) = mibBuilder.importSymbols(  # type: ignore
            "SNMP-TARGET-MIB",
            "snmpTargetParamsMPModel",
            "snmpTargetParamsSecurityModel",
            "snmpTargetParamsSecurityName",
            "snmpTargetParamsSecurityLevel",
        )

        tblIdx = snmpTargetParamsEntry.getInstIdFromIndices(paramsName)

        try:
            snmpTargetParamsMPModel = snmpTargetParamsMPModel.getNode(
                snmpTargetParamsMPModel.name + tblIdx
            ).syntax
            snmpTargetParamsSecurityModel = snmpTargetParamsSecurityModel.getNode(
                snmpTargetParamsSecurityModel.name + tblIdx
            ).syntax
            snmpTargetParamsSecurityName = snmpTargetParamsSecurityName.getNode(
                snmpTargetParamsSecurityName.name + tblIdx
            ).syntax
            snmpTargetParamsSecurityLevel = snmpTargetParamsSecurityLevel.getNode(
                snmpTargetParamsSecurityLevel.name + tblIdx
            ).syntax
        except NoSuchInstanceError:
            raise SmiError("Parameters %s not configured at LCD" % paramsName)

        nameToParamsMap[paramsName] = (
            snmpTargetParamsMPModel,
            snmpTargetParamsSecurityModel,
            snmpTargetParamsSecurityName,
            snmpTargetParamsSecurityLevel,
        )

        cache["id"] = snmpTargetParamsEntry.branchVersionId

    return nameToParamsMap[paramsName]


def getTargetInfo(snmpEngine: SnmpEngine, snmpTargetAddrName):
    # Transport endpoint
    (
        snmpTargetAddrTDomain,
        snmpTargetAddrTAddress,
        snmpTargetAddrTimeout,
        snmpTargetAddrRetryCount,
        snmpTargetAddrParams,
    ) = getTargetAddr(snmpEngine, snmpTargetAddrName)

    (
        snmpTargetParamsMPModel,
        snmpTargetParamsSecurityModel,
        snmpTargetParamsSecurityName,
        snmpTargetParamsSecurityLevel,
    ) = getTargetParams(snmpEngine, snmpTargetAddrParams)

    return (
        snmpTargetAddrTDomain,
        snmpTargetAddrTAddress,
        snmpTargetAddrTimeout,
        snmpTargetAddrRetryCount,
        snmpTargetParamsMPModel,
        snmpTargetParamsSecurityModel,
        snmpTargetParamsSecurityName,
        snmpTargetParamsSecurityLevel,
    )


def getNotificationInfo(snmpEngine: SnmpEngine, notificationTarget):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    (snmpNotifyEntry,) = mibBuilder.importSymbols(  # type: ignore
        "SNMP-NOTIFICATION-MIB", "snmpNotifyEntry"
    )

    cache: "dict[str, Any] | None" = snmpEngine.getUserContext("getNotificationInfo")
    if cache is None:
        cache = {"id": -1}
        snmpEngine.setUserContext(getNotificationInfo=cache)

    if cache["id"] != snmpNotifyEntry.branchVersionId:
        cache["targetToNotifyMap"] = {}  # type: ignore

    targetToNotifyMap = cache["targetToNotifyMap"]

    if notificationTarget not in targetToNotifyMap:
        (snmpNotifyTag, snmpNotifyType) = mibBuilder.importSymbols(  # type: ignore
            "SNMP-NOTIFICATION-MIB", "snmpNotifyTag", "snmpNotifyType"
        )

        tblIdx = snmpNotifyEntry.getInstIdFromIndices(notificationTarget)

        try:
            snmpNotifyTag = snmpNotifyTag.getNode(snmpNotifyTag.name + tblIdx).syntax
            snmpNotifyType = snmpNotifyType.getNode(snmpNotifyType.name + tblIdx).syntax

        except NoSuchInstanceError:
            raise SmiError("Target %s not configured at LCD" % notificationTarget)

        targetToNotifyMap[notificationTarget] = (snmpNotifyTag, snmpNotifyType)

        cache["id"] = snmpNotifyEntry.branchVersionId

    return targetToNotifyMap[notificationTarget]


def getTargetNames(snmpEngine: SnmpEngine, tag):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    (snmpTargetAddrEntry,) = mibBuilder.importSymbols(  # type: ignore
        "SNMP-TARGET-MIB", "snmpTargetAddrEntry"
    )

    cache: "dict[str, Any] | None" = snmpEngine.getUserContext("getTargetNames")
    if cache is None:
        cache = {"id": -1}
        snmpEngine.setUserContext(getTargetNames=cache)

    if cache["id"] == snmpTargetAddrEntry.branchVersionId:
        tagToTargetsMap = cache["tagToTargetsMap"]
    else:
        cache["tagToTargetsMap"] = {}

        tagToTargetsMap = cache["tagToTargetsMap"]

        (
            SnmpTagValue,
            snmpTargetAddrName,
            snmpTargetAddrTagList,
        ) = mibBuilder.importSymbols(  # type: ignore
            "SNMP-TARGET-MIB",
            "SnmpTagValue",
            "snmpTargetAddrName",
            "snmpTargetAddrTagList",
        )
        mibNode = snmpTargetAddrTagList
        while True:
            try:
                mibNode = snmpTargetAddrTagList.getNextNode(mibNode.name)
            except NoSuchInstanceError:
                break

            idx = mibNode.name[len(snmpTargetAddrTagList.name) :]

            _snmpTargetAddrName = snmpTargetAddrName.getNode(
                snmpTargetAddrName.name + idx
            ).syntax

            for _tag in mibNode.syntax.asOctets().split():
                _tag = SnmpTagValue(_tag)
                if _tag not in tagToTargetsMap:
                    tagToTargetsMap[_tag] = []
                tagToTargetsMap[_tag].append(_snmpTargetAddrName)

        cache["id"] = snmpTargetAddrEntry.branchVersionId

    if tag not in tagToTargetsMap:
        raise SmiError("Transport tag %s not configured at LCD" % tag)

    return tagToTargetsMap[tag]


# convert cmdrsp/cmdgen into this api
