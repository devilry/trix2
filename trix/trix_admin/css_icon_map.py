from cradmin_legacy import css_icon_map

#: Font-awesome icon map for the ``cradmin_icon`` template tag.
# NOTE this is font-awesome v4 syntax, this is because cradmin uses font-awesome 4
css_icon_map.FONT_AWESOME.update({'arrow-up': 'fa fa-arrow-up',
                                  'database': 'fa fa-database',
                                  'link': 'fa fa-link',
                                  'chart-bar': 'fa fa-chart-bar',
                                  'wrench': 'fa fa-wrench'})
FONT_AWESOME = css_icon_map.FONT_AWESOME
