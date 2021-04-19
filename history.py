class History:
    post_type = 'turtle'    # 'turtle' or 'product'
    turtle = 0              # last turtle post used
    product = 0             # last product post used

    # swaps post type from 'turtle' to 'product'
    def swap(self):
        self.post_type = 'turtle' if self.post_type == 'product' else 'product'

    # either increment post or loop back to first post for either turtle or product history
    def update_post_number(self, length):
        if self.post_type == 'turtle':
            self.turtle = 1 if self.turtle + 1 > length else self.turtle + 1

        elif self.post_type == 'product':
            self.product = 1 if self.product + 1 > length else self.product + 1
