from pydantic import BaseModel, HttpUrl, Field, computed_field
from typing import List, Optional
import re


class Brand(BaseModel):
    type: str = Field(alias="@type")
    name: str


class Offer(BaseModel):
    type: str = Field(alias="@type")
    price: float
    price_currency: str = Field(alias="priceCurrency")


class Vinmonopolprodukt(BaseModel):
    name: str
    description: str
    offers: Offer
    image: HttpUrl
    brand: Brand
    url: str
    keywords: List[str] = []
    size: str
    abv: float
    country_of_origin: str = Field(alias="countryOfOrigin")
    color: Optional[str] = None

    def _parse_size(self) -> float:
        """Parse the size string and return volume in liters."""
        match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*(cl|ml|l)", self.size.lower())
        if not match:
            raise ValueError(
                f"Unable to parse size '{self.size}'. Expected format: '<amount> <unit>' where unit is one of 'cl', 'ml', 'l'."
            )

        amount, unit = match.groups()
        amount = float(amount.replace(",", "."))

        if unit == "cl":
            return amount / 100
        elif unit == "ml":
            return amount / 1000
        elif unit == "l":
            return amount
        else:
            raise ValueError(f"Unknown unit: {unit}")

    @computed_field
    def price_per_liter(self) -> float:
        """Calculate the price per liter."""
        volume_in_liters = self._parse_size()
        return round(self.offers.price / volume_in_liters, 2)

    @computed_field
    def alcohol_per_nok(self) -> float:
        """Calculate milliliters of pure alcohol per NOK."""
        return round(
            (self.abv / 100) * (self._parse_size() * 1000) / self.offers.price, 6
        )

    @computed_field
    def absolute_url(self) -> str:
        return f"https://www.vinmonopolet.no{self.url}"
