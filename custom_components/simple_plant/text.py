# MIT LICENCE - Copyright (c) 2026  ndesgranges
# pylint: disable=duplicate-code
"""Text platform for simple_plant."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.text import (
    TextEntity,
    TextEntityDescription,
    TextMode,
)

from .const import NOTES_MAX_LENGTH
from .entity import SimplePlantStoredEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


ENTITY_DESCRIPTIONS = (
    TextEntityDescription(
        key="notes",
        translation_key="notes",
        icon="mdi:note-text-outline",
        mode=TextMode.TEXT,
        native_min=0,
        native_max=NOTES_MAX_LENGTH,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the text platform."""
    async_add_entities(
        SimplePlantText(hass, entry, entity_description)
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SimplePlantText(SimplePlantStoredEntity, TextEntity):  # pylint: disable=abstract-method
    """simple_plant text class, used for free-form plant notes."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: TextEntityDescription,
    ) -> None:
        """Initialize the text class."""
        super().__init__(hass, entry, description, "text")
        self._fallback_value = str(entry.data.get("notes") or "")
        self._attr_native_value: str | None = None

    async def _restore_value(self, value: Any) -> None:
        """Restore a stored or fallback value."""
        await self.async_set_value(str(value))

    async def async_set_value(self, value: str) -> None:
        """Change the notes."""
        self._attr_native_value = value
        self.async_write_ha_state()
        # Save to persistent storage
        if self.unique_id is not None:
            await self.coordinator.async_store_value(self.unique_id, value)
