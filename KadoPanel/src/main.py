# -*- coding: utf-8 -*-

from Screens.MessageBox import MessageBox

def main(session, **kwargs):
    session.open(
        MessageBox,
        "Welcome to Kado Panel\nProfessional Enigma2",
        MessageBox.TYPE_INFO
    )
