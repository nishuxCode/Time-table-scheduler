import random
import copy
from .TimeTable import TimeTable

class Gene:
    def __init__(self, i, data):
        self.id = i # Student Group ID
        self.days = data.days_per_week
        self.hours = data.hours_per_day
        self.break_slot = getattr(data, 'break_slot', 3)
        total_slots = self.days * self.hours
        
        # बेस इंडेक्स जहाँ से इस ग्रुप के स्लॉट शुरू होते हैं
        base_idx = i * total_slots
        
        # १. स्लॉट्स को पहचानें और ब्लॉक बनाएं
        blocks = []
        temp_slots = TimeTable.slot[base_idx : base_idx + total_slots]
        
        # विषयों को ग्रुप करें (जैसे 2 घंटे की लैब को एक ब्लॉक मानें)
        processed = [False] * total_slots
        for j in range(total_slots):
            if processed[j]: continue
            
            current_block = [base_idx + j]
            processed[j] = True
            
            slot_obj = temp_slots[j]
            if slot_obj is not None:
                # अगले स्लॉट्स देखें क्या वो वही सब्जेक्ट हैं?
                for k in range(j + 1, total_slots):
                    next_obj = temp_slots[k]
                    if next_obj and next_obj.subject == slot_obj.subject:
                        current_block.append(base_idx + k)
                        processed[k] = True
                    else:
                        break
            blocks.append(current_block)

        # २. ग्रिड तैयार करें
        self.grid = [None] * total_slots

        def can_place(pos, length):
            if pos + length > total_slots: return False
            # क्या यह एक ही दिन में है?
            if (pos // self.hours) != ((pos + length - 1) // self.hours): return False
            # क्या यह ब्रेक स्लॉट को काट रहा है?
            start_h = pos % self.hours
            if start_h < self.break_slot and (start_h + length) > self.break_slot: return False
            # क्या वहां पहले से कुछ है?
            for k in range(length):
                if self.grid[pos + k] is not None: return False
            return True

        # ३. बड़े ब्लॉक्स (Labs) पहले रखें
        large_blocks = [b for b in blocks if len(b) > 1]
        small_blocks = [b for b in blocks if len(b) == 1]
        
        random.shuffle(large_blocks)
        for block in large_blocks:
            length = len(block)
            placed = False
            for _ in range(100): # 100 random attempts
                pos = random.randint(0, total_slots - length)
                if can_place(pos, length):
                    for k in range(length): self.grid[pos+k] = block[k]
                    placed = True
                    break
            if not placed: # Emergency placement
                for pos in range(total_slots - length + 1):
                    if can_place(pos, length):
                        for k in range(length): self.grid[pos+k] = block[k]
                        placed = True
                        break

        # ४. बाकी सिंगल स्लॉट्स भरें
        for block in small_blocks:
            idx = block[0]
            for pos in range(total_slots):
                if self.grid[pos] is None:
                    self.grid[pos] = idx
                    break

        # final slot assignment
        self.slotno = self.grid

    def deep_clone(self):
        return copy.deepcopy(self)
