from w3fu.storage import Document, Property


DAYS = 7
SECONDS_PER_SLOT = 5 * 60
SLOTS_PER_DAY = 24 * 3600 / SECONDS_PER_SLOT


class Schedule(Document):

    slots = Property('slots', default=[], hidden=True)

    def get_state(self, day, slot):
        try:
            return self.slots[day][slot]
        except IndexError:
            return 1

    def set_state(self, day, slot, state):
        if not self.slots:
            for _ in range(DAYS):
                self.slots.append([1] * SLOTS_PER_DAY)
        self.slots[day][slot] = state
        pass

    def merge(self, party):
        for day in range(DAYS):
            for slot in range(SLOTS_PER_DAY):
                state = '_'.join(['s', str(slot), str(day)]) in party
                self.set_state(day, slot, 1 if state else 0)

    def dump(self):
        out = []
        for slot in range(SLOTS_PER_DAY):
            m = (slot * SECONDS_PER_SLOT) // 60
            h, m = divmod(m, 60)
            label = '{0:02}:{1:02}'.format(h, m)
            slots = {'label': label,
                     'by_day': [self.get_state(day, slot)
                                for day in range(DAYS)]}
            out.append(slots)
        return out
