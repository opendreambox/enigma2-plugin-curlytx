# -*- coding: utf-8 -*-
# CurlyTx configuration
# Copyright (C) 2011 Christian Weiske <cweiske@cweiske.de>
# License: GPLv3 or later

from Components.config import config, ConfigEnableDisable, ConfigYesNo, ConfigSelection, ConfigNumber, ConfigText, ConfigSubsection, ConfigSubList, ConfigInteger

def createPage():
    """ Create and return a configuration page object """
    s = ConfigSubsection()
    s.uri   = ConfigText(default="http://", fixed_size=False)
    s.title = ConfigText(
        default = "Page #" + str(len(config.plugins.CurlyTx.pages) + 1),
        fixed_size = False
        )
    s.fontSize = ConfigInteger(20, (1, 100))
    return s

def loadDefaultPageOptions():
    defaults = []
    for i in range(0, len(config.plugins.CurlyTx.pages)):
        defaults.append((str(i), config.plugins.CurlyTx.pages[i].title.value))
    if hasattr(config.plugins.CurlyTx, "defaultPage"):
        config.plugins.CurlyTx.defaultPage.setChoices(defaults, "0")
    else:
        config.plugins.CurlyTx.defaultPage = ConfigSelection(defaults, "0")

def feedPagesToConfig(pages):
    """ save pages from atom feed into config. """
    if len(pages) == 0:
        return

    del config.plugins.CurlyTx.pages[:]

    for pageData in pages:
        page = createPage()
        config.plugins.CurlyTx.pages.append(page)
        page.title.setValue(pageData["title"])
        page.uri.setValue(pageData["url"])

def feedSettingsToConfig(settings):
    changed = False
    if 'enableSettings' in settings and config.plugins.CurlyTx.enableSettings.getValue() != settings['enableSettings']:
        config.plugins.CurlyTx.enableSettings.setValue(int(settings['enableSettings']))
        changed = True

    if changed:
        config.plugins.CurlyTx.save()

def savePageConfig():
    for i in range(0, len(config.plugins.CurlyTx.pages)):
        config.plugins.CurlyTx.pages[i].save()

    config.plugins.CurlyTx.pages.save()


#configuration setup
config.plugins.CurlyTx = ConfigSubsection()
config.plugins.CurlyTx.menuMain = ConfigYesNo(default = True)
config.plugins.CurlyTx.menuExtensions = ConfigYesNo(default = False)
config.plugins.CurlyTx.enableSettings = ConfigEnableDisable(default = True)
config.plugins.CurlyTx.menuTitle = ConfigText(default = "CurlyTx", fixed_size = False)
config.plugins.CurlyTx.feedUrl = ConfigText(default = "", fixed_size = False)
config.plugins.CurlyTx.pages = ConfigSubList()
for id,value in config.plugins.CurlyTx.pages.stored_values.iteritems():
    config.plugins.CurlyTx.pages.append(createPage())
loadDefaultPageOptions()
