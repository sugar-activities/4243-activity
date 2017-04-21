# -*- coding: utf-8 -*-

import logging
import olpcgames
import pygame
import gtk

from olpcgames import mesh
from olpcgames import util

from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarBox
from gettext import gettext as _

class PacmanActivity(olpcgames.PyGameActivity):
    game_name = 'game'
    game_title = _('Pacman')
    game_size = None    # Let olpcgames pick a nice size for us

    def __init__(self, handle):
        super(PacmanActivity, self).__init__(handle)

        # This code was copied from olpcgames.activity.PyGameActivity
        def shared_cb(*args, **kwargs):
            logging.info('shared: %s, %s', args, kwargs)
            try:
                mesh.activity_shared(self)
            except Exception, err:
                logging.error('Failure signaling activity sharing'
                              'to mesh module: %s', util.get_traceback(err))
            else:
                logging.info('mesh activity shared message sent,'
                             ' trying to grab focus')
            try:
                self._pgc.grab_focus()
            except Exception, err:
                logging.warn('Focus failed: %s', err)
            else:
                logging.info('asserting focus')
                assert self._pgc.is_focus(), \
                    'Did not successfully set pygame canvas focus'
            logging.info('callback finished')

        def joined_cb(*args, **kwargs):
            logging.info('joined: %s, %s', args, kwargs)
            mesh.activity_joined(self)
            self._pgc.grab_focus()
        self.connect('shared', shared_cb)
        self.connect('joined', joined_cb)

        if self.get_shared():
            # if set at this point, it means we've already joined (i.e.,
            # launched from Neighborhood)
            joined_cb()

    def build_toolbar(self):
        """Build our Activity toolbar for the Sugar system."""

        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()

        self.connect("destroy", self.__stop_pygame)

        return toolbar_box

    def __stop_pygame(self, widget):
        pygame.quit()

