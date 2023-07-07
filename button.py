'''
CITATION: This button class is based on code from https://github.com/baraltech/Menu-System-PyGame

as introduced in this YouTube video: https://www.youtube.com/watch?v=GMBqjxcKogA
'''
class BaseButton():
	def render(self) -> None:
		pass

class Button(BaseButton):
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def render(self, screen, mouse_position):
		color = self.base_color

		if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
			color = self.hovering_color

		self.text = self.font.render(self.text_input, True, color)

		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def is_clicked(self, position):
		return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)

class BaseButtonDecorator(BaseButton):
	_button: BaseButton = None
	
	def __init__(self, button: BaseButton) -> None:
		self._button = button

	@property
	def button(self) -> BaseButton:
		return self._button

	def render(self) -> None:
		return self._button.render()
