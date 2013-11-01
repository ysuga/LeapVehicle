#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file LeapVehicle.py
 @brief Leap Motion RTC
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import ssr

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
leaptest_spec = ["implementation_id", "LeapVehicle", 
		 "type_name",         "LeapVehicle", 
		 "description",       "Leap Motion RTC", 
		 "version",           "1.0.0", 
		 "vendor",            "Sugar Sweet Robotics", 
		 "category",          "input", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.debug", "0",
		 "conf.__widget__.debug", "text",
		 ""]
# </rtc-template>

##
# @class LeapVehicle
# @brief Leap Motion RTC
# 
# 
class LeapVehicle(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_frame = ssr.Frame(0, 0, [], [])
		self._d_vel = RTC.TimedVelocity2D(RTC.Time(0,0), RTC.Velocity2D(0, 0, 0))
		"""
		"""
		
		self._frameIn = OpenRTM_aist.InPort("frame", self._d_frame)

		self._velOut = OpenRTM_aist.OutPort("vel", self._d_vel)
		#circle = ssr.CircleGesture(0, 0, 0, ssr.Vector(0,0,0), ssr.Vector(0,0,0), 0)
		#swipe  = ssr.SwipeGesture(0, ssr.Vector(0, 0,0 ), 0)
		#key    = ssr.KeyTapGesture(0, ssr.Vector(0, 0, 0), ssr.Vector(0, 0, 0))
		#screen = ssr.ScreenTapGesture(0, ssr.Vector(0, 0, 0), ssr.Vector(0, 0, 0))
		#self._d_gesture = ssr.GestureFrame(0, 0, ssr.TYPE_INVALID, circle, swipe, key, screen)
		"""
		"""
		#self._gestureIn = OpenRTM_aist.InPort("gesture", self._d_gesture)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  debug
		 - DefaultValue: 0
		"""
		self._debug = [0]
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("debug", self._debug, "0")
		
		# Set InPort buffers
		self.addInPort("frame",self._frameIn)
		#self.addInPort("gesture",self._gestureIn)

		# Set OutPort buffers
		self.addOutPort("vel", self._velOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
		self._d_vel.data.vx = 0
		self._d_vel.data.vy = 0
		self._d_vel.data.va = 0
		self._velOut.write()
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		self._d_vel.data.vx = 0
		self._d_vel.data.vy = 0
		self._d_vel.data.va = 0
		self._velOut.write()
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		if self._frameIn.isNew():
			v = self._frameIn.read()
			#print '[RTC::LeapVehicle] Frame - %s Timestamp - %s' % (v.id, v.timestamp)
			if len(v.hands) == 0:
				#print '[RTC::LeapVehicle] No hands'
				self._d_vel.data.vx = 0
				self._d_vel.data.vy = 0
				self._d_vel.data.va = 0
				self._velOut.write()
				pass
			else:
				if len(v.gestures) == 0:
					for i, hand in enumerate(v.hands):
						#print '[RTC::LeapVehicle] Hand[%s] - Position(%s) - Direction(%s) - Fingers(%s)' % (i, repr(hand.palmPosition), repr(hand.palmDirection), len(hand.fingers))
					
						#print '[RTC::LeapVehicle] Hand %s' % i
						if len(hand.fingers) == 2:
							#print '[RTC::LeapVehicle] Two Fingers'
							self._d_vel.data.vx = 0.1
							self._d_vel.data.vy = 0
							self._d_vel.data.va = -hand.palmDirection.x
							self._velOut.write()
							pass
						if len(hand.fingers) == 3:
							#print '[RTC::LeapVehicle] Two Fingers'
							self._d_vel.data.vx = 0.3
							self._d_vel.data.vy = 0
							self._d_vel.data.va = -hand.palmDirection.x
							self._velOut.write()
							pass
						if len(hand.fingers) == 4:
							#print '[RTC::LeapVehicle] Two Fingers'
							self._d_vel.data.vx = 0.5
							self._d_vel.data.vy = 0
							self._d_vel.data.va = -hand.palmDirection.x
							self._velOut.write()
							pass

				else: # if gesture
					for i, gesture in enumerate(v.gestures):
						type_str = "invalid"
						if gesture.type == ssr.TYPE_INVALID:
							#print '[RTC::LeapVehicle] InvalidGesture'
							pass
						elif gesture.type == ssr.TYPE_SWIPE:
					#print 'RTC::LeapVehicle] SwipeGesture'
							#print '[RTC::LeapVehicle] SwipeGesture - state %s, direction %s, speed %s' % (gesture.swipe.state, gesture.swipe.direction, gesture.swipe.speed)
							pass
						elif gesture.type == ssr.TYPE_CIRCLE:
					#print 'RTC::LeapVehicle] CircleGesture'
							#print '[RTC::LeapVehicle] CircleGesture - state %s, progress %s, radius %s, center %s, normal %s' % (gesture.circle.state, gesture.circle.progress, gesture.circle.radius, gesture.circle.center, gesture.circle.normal)
							#gesture.circle.
							self._d_vel.data.vx = 0
							self._d_vel.data.vy = 0
							self._d_vel.data.va = gesture.circle.normal.z
							self._velOut.write()
							pass

							pass
						elif gesture.type == ssr.TYPE_SCREEN_TAP:
					#print 'RTC::LeapVehicle] ScreenTapGesture'
							#print '[RTC::LeapVehicle] ScreentapGesture - state %s, direction %s, position %s' % (gesture.screen.state, gesture.screen.direction, gesture.screen.position)
							pass
						elif gesture.type == ssr.TYPE_KEY_TAP:
					#print 'RTC::LeapVehicle] KeyTapGesture'
							#print '[RTC::LeapVehicle] KeytapGesture - state %s, direction %s, position %s' % (gesture.key.state, gesture.key.direction, gesture.key.position)
							pass
				

		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def LeapVehicleInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=leaptest_spec)
    manager.registerFactory(profile,
                            LeapVehicle,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    LeapVehicleInit(manager)

    # Create a component
    comp = manager.createComponent("LeapVehicle")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

