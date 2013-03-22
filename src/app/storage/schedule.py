from w3fu.storage import Document, Property


SLOT_SIZE = 5 * 60
SLOTS_PER_DAY = 24 * 3600 / SLOT_SIZE


class Schedule(Document):

    slots = Property('slots', default=[], hidden=True)

    def flat_slots(self):
        out = []
        for day in range(7):
            try:
                out.append(self.slots[day])
            except IndexError:
                out.append([1] * SLOTS_PER_DAY)
        return out

    def dump(self):
        out = []
        flat_slots = self.flat_slots()
        for slot in range(SLOTS_PER_DAY):
            m = (slot * SLOT_SIZE) // 60
            h, m = divmod(m, 60)
            label = '{0:02}:{1:02}'.format(h, m)
            slots = {'label': label,
                     'by_day': [flat_slots[day][slot]
                                for day in range(7)]}
            out.append(slots)
        return out
