from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List, Optional
import re
from humps import camelize


def to_camel(string: str) -> str:
    return camelize(string)


class BaseModelCamel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={},  # This ensures proper JSON encoding
        ser_json_timedelta="iso8601",  # Optional: for consistent datetime serialization
    )

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(by_alias=True, **kwargs)


class Characteristic(BaseModelCamel):
    name: str
    readable_value: str
    value: str


class Ingredient(BaseModelCamel):
    code: str
    formatted_value: str
    readable_value: str


class GoodFor(BaseModelCamel):
    code: str
    name: str


class StoragePotential(BaseModelCamel):
    code: str
    formatted_value: str


class Style(BaseModelCamel):
    code: str
    description: str
    name: str


class Trait(BaseModelCamel):
    formatted_value: str
    name: str
    readable_value: str


class Content(BaseModelCamel):
    characteristics: Optional[List[Characteristic]] = None
    ingredients: Optional[List[Ingredient]] = None
    is_good_for: Optional[List[GoodFor]] = None
    storage_potential: Optional[StoragePotential] = None
    style: Optional[Style] = None
    traits: List[Trait]


class District(BaseModelCamel):
    code: str
    name: str
    search_query: str
    url: str


class Image(BaseModelCamel):
    alt_text: str
    format: str
    image_type: str
    url: str


class Price(BaseModelCamel):
    formatted_value: str
    readable_value: str
    value: float


class Category(BaseModelCamel):
    code: str
    name: str


class Country(BaseModelCamel):
    code: str
    name: str
    search_query: str
    url: str


class Producer(BaseModelCamel):
    code: str
    name: str
    search_query: str
    url: str


class Volume(BaseModelCamel):
    formatted_value: str
    readable_value: str
    value: Optional[float]


class VinmonopolProduct(BaseModelCamel):
    age_limit: int
    allergens: Optional[str] = None
    bio_dynamic: bool
    buyable: bool
    code: str
    color: Optional[str] = None
    content: Content
    cork: Optional[str] = None
    description: str
    distributor: str
    distributor_id: int
    district: Optional[District] = None
    eco: bool
    environmental_packaging: bool
    expired: bool
    fair_trade: bool
    gluten: bool
    images: List[Image]
    kosher: bool
    litre_price: Price
    main_category: Category
    main_country: Optional[Country] = None
    main_producer: Producer
    name: str
    package_type: Optional[str] = None
    price: Price
    product_selection: str
    release_mode: bool
    similar_products: bool
    smell: Optional[str] = None
    status: str
    status_notification: bool
    summary: str
    sustainable: bool
    taste: Optional[str] = None
    url: str
    volume: Volume
    whole_saler: str
    year: Optional[str] = None

    def _parse_size(self) -> float:
        """Parse the size string and return volume in liters."""
        size = self.volume.formatted_value
        match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*(cl|ml|l)", size.lower())
        if not match:
            raise ValueError(
                f"Unable to parse size '{size}'. Expected format: '<amount> <unit>' where unit is one of 'cl', 'ml', 'l'."
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
    @property
    def parsed_size(self) -> float:
        return self._parse_size()

    @computed_field
    @property
    def price_per_liter(self) -> float:
        return round(self.price.value / self.parsed_size, 2)

    @computed_field
    @property
    def alcohol_per_nok(self) -> Optional[float]:
        alcohol_trait = next(
            (trait for trait in self.content.traits if trait.name == "Alkohol"), None
        )
        if alcohol_trait:
            abv = float(
                alcohol_trait.readable_value.rstrip(" prosent").replace(",", ".")
            )
            return round((abv / 100) * (self.parsed_size * 1000) / self.price.value, 6)
        return None

    @computed_field
    @property
    def absolute_url(self) -> str:
        return f"https://www.vinmonopolet.no{self.url}"
