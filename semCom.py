#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: semanticCom
# Author: Berkehan Ercan
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class semCom(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "semanticCom", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("semanticCom")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "semCom")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.samp_rate = samp_rate = 1000000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1.0, samp_rate,samp_rate/sps, 0.5, (11*sps))
        self.payload_length = payload_length = 256
        self.freqs = freqs = 1
        self.channel_time = channel_time = 1
        self.channel_noise = channel_noise = 0.1
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bpsk.set_npwr(1.0)
        self.barker11 = barker11 = (1,1,1,0,0,0,1,0,0,1,0)

        ##################################################
        # Blocks
        ##################################################

        self.tab_qt = Qt.QTabWidget()
        self.tab_qt_widget_0 = Qt.QWidget()
        self.tab_qt_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_qt_widget_0)
        self.tab_qt_grid_layout_0 = Qt.QGridLayout()
        self.tab_qt_layout_0.addLayout(self.tab_qt_grid_layout_0)
        self.tab_qt.addTab(self.tab_qt_widget_0, 'Frequency Domain')
        self.tab_qt_widget_1 = Qt.QWidget()
        self.tab_qt_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_qt_widget_1)
        self.tab_qt_grid_layout_1 = Qt.QGridLayout()
        self.tab_qt_layout_1.addLayout(self.tab_qt_grid_layout_1)
        self.tab_qt.addTab(self.tab_qt_widget_1, 'Time Domain')
        self.tab_qt_widget_2 = Qt.QWidget()
        self.tab_qt_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_qt_widget_2)
        self.tab_qt_grid_layout_2 = Qt.QGridLayout()
        self.tab_qt_layout_2.addLayout(self.tab_qt_grid_layout_2)
        self.tab_qt.addTab(self.tab_qt_widget_2, 'Constellation Plot')
        self.top_layout.addWidget(self.tab_qt)
        self._freqs_range = qtgui.Range(1-0.001, 1+0.001, 0.00001, 1, 200)
        self._freqs_win = qtgui.RangeWidget(self._freqs_range, self.set_freqs, "Frequency Shift", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freqs_win)
        self._channel_time_range = qtgui.Range(1-0.001, 1+0.001, 0.00001, 1, 200)
        self._channel_time_win = qtgui.RangeWidget(self._channel_time_range, self.set_channel_time, "Channel Time Shift", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._channel_time_win)
        self._channel_noise_range = qtgui.Range(0, 3, 0.001, 0.1, 200)
        self._channel_noise_win = qtgui.RangeWidget(self._channel_noise_range, self.set_channel_noise, "Channel Noise Voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._channel_noise_win)
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                (samp_rate/sps),
                0.5,
                1000))
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            10000, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(True)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Corr Magnitude', 'Re{Corr}', 'Im{Corr}', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.tab_qt_layout_1.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            16384, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.01)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "packet_len")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Received Bits', 'CRC Check', 'BER', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_qt_layout_1.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            16384, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_qt_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            2048, #size
            "Constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.01)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["green", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_qt_layout_2.addWidget(self._qtgui_const_sink_x_0_win)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 0.0628, rrc_taps, 32, 16, 1.5, (sps//2))
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", False)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(0.065, 2, False)
        self.digital_corr_est_cc_0 = digital.corr_est_cc((1,1,1,-1,-1,-1,1,-1,-1,1,-1), sps, 1, 4, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=bpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.50,
            verbose=False,
            log=False,
            truncate=True)
        self.digital_constellation_modulator_0.set_block_alias("bpsk_mod")
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=channel_noise,
            frequency_offset=freqs,
            epsilon=channel_time,
            taps=[1],
            noise_seed=213,
            block_tags=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(barker11, True, 1, )
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(8, gr.GR_MSB_FIRST)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_mux_1 = blocks.tagged_stream_mux(gr.sizeof_char*1, "packet_len", 0)
        self.blocks_stream_to_tagged_stream_1 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, len(barker11), "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 256, "packet_len")
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 2, 123)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_1, 0), (self.blocks_tagged_stream_mux_1, 0))
        self.connect((self.blocks_tagged_stream_mux_1, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_tagged_stream_1, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self.blocks_complex_to_float_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_1, 1))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.digital_corr_est_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "semCom")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(1.0, self.samp_rate, self.samp_rate/self.sps, 0.5, (11*self.sps)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), 0.5, 1000))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rrc_taps(firdes.root_raised_cosine(1.0, self.samp_rate, self.samp_rate/self.sps, 0.5, (11*self.sps)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), 0.5, 1000))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_payload_length(self):
        return self.payload_length

    def set_payload_length(self, payload_length):
        self.payload_length = payload_length

    def get_freqs(self):
        return self.freqs

    def set_freqs(self, freqs):
        self.freqs = freqs
        self.channels_channel_model_0.set_frequency_offset(self.freqs)

    def get_channel_time(self):
        return self.channel_time

    def set_channel_time(self, channel_time):
        self.channel_time = channel_time
        self.channels_channel_model_0.set_timing_offset(self.channel_time)

    def get_channel_noise(self):
        return self.channel_noise

    def set_channel_noise(self, channel_noise):
        self.channel_noise = channel_noise
        self.channels_channel_model_0.set_noise_voltage(self.channel_noise)

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk
        self.digital_constellation_decoder_cb_0.set_constellation(self.bpsk)

    def get_barker11(self):
        return self.barker11

    def set_barker11(self, barker11):
        self.barker11 = barker11
        self.blocks_stream_to_tagged_stream_1.set_packet_len(len(self.barker11))
        self.blocks_stream_to_tagged_stream_1.set_packet_len_pmt(len(self.barker11))
        self.blocks_vector_source_x_0.set_data(self.barker11, )




def main(top_block_cls=semCom, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
