import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and crete game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the "Play" button
        self.play_button = Button(self, "Play the game!")

    def _check_events(self):
        """Watching for keyboard and mouse events"""
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif keys[pygame.K_p] and not self.stats.game_active:
                self._start_game()

        # Q to quit
        if keys[pygame.K_q]:
            sys.exit()
        # Space to fire
        if keys[pygame.K_SPACE]:
            self._fire_bullet()

        # Up, down, left, right to move the ship

        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.ship.moving_right = True
            self.ship.moving_up = True
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.ship.moving_right = True
            self.ship.moving_down = True
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.ship.moving_left = True
            self.ship.moving_up = True
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.ship.moving_left = True
            self.ship.moving_down = True
        elif keys[pygame.K_RIGHT]:
            self.ship.moving_right = True
        elif keys[pygame.K_LEFT]:
            self.ship.moving_left = True
        elif keys[pygame.K_UP]:
            self.ship.moving_up = True
        elif keys[pygame.K_DOWN]:
            self.ship.moving_down = True
        else:
            self.ship.moving_right = False
            self.ship.moving_left = False
            self.ship.moving_up = False
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when user clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if not self.stats.game_active and button_clicked:
            self._start_game()

    def _start_game(self):
        """Initializing starting a game"""
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True

        # Clear any remaining aliens and bullets from the screen
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor when the game is active
        pygame.mouse.set_visible(False)



    def _fire_bullet(self):
        """Create a new bullet and add the bullet to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullets position and get rid of old bullets"""
        # Update bullets position
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 1.3 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create an alien and find the number of aliens in the row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (1.7 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(int(number_rows)):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the position of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting bottom of the screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()

    def _check_aliens_bottom(self):
        """Check if any aliens reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same way as ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to a ship being hit by alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            # Clear any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)    # Setting the cursor visible when game is over

    def _update_screen(self):
        # Update assets on the screen, and flip to the new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
