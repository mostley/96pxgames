# -*- coding: utf8 -*- 


class StateChange(object):
    Unknown = 0
    Enter = 1
    Leave = 2


class StateMachine(object):
    def __init__(self, states, state_change_callback=None):
        self.states = {}
        for state in states:
            self.states[state.name] = state

        self.currentState = None
        self.state_change_callback = state_change_callback

    def setState(self, name):
        if not name in self.states:
            raise Exception("state '" + name + "' does not exist")

        new_state = self.states[name]
        old_state = self.currentState

        if self.currentState:
            self.currentState.onLeave(new_state)

        self.currentState = new_state
        self.currentState.onEnter(old_state)
        self.state_change_callback(self.currentState, StateChange.Enter)

    def update(self, dt):
        if self.currentState:
            self.currentState.update(dt)

            if self.currentState.ended and not self.state_change_callback is None:
                state = self.currentState
                self.currentState = None
                self.state_change_callback(state, StateChange.Leave)

    def draw(self, rgb):
        if self.currentState:
            self.currentState.draw(rgb)

    def onAxisChanged(self, player, x_axis, y_axis, previous_x_axis, previous_y_axis):
        if self.currentState:
            self.currentState.onAxisChanged(player, x_axis, y_axis, previous_x_axis, previous_y_axis)

    def onClampedAxisChanged(self, player, x, y):
        if self.currentState:
            self.currentState.onClampedAxisChanged(player, x, y)

    def onButtonChanged(self, player, a_button, b_button, previous_a_button, previous_b_button):
        if self.currentState:
            self.currentState.onButtonChanged(player, a_button, b_button, previous_a_button, previous_b_button)