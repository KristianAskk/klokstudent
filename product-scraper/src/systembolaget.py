from pydantic import BaseModel, Field, computed_field
from typing import List, Optional
from datetime import datetime, time


class SystembolagetImage(BaseModel):
    file_type: Optional[str] = Field(alias="fileType")
    image_url: Optional[str] = Field(alias="imageUrl")
    size: Optional[str]


class Systembolagetprodukt(BaseModel):
    product_id: str = Field(alias="productId")
    product_number: str = Field(alias="productNumber")
    product_number_short: str = Field(alias="productNumberShort")
    product_name_bold: str = Field(alias="productNameBold")
    product_name_thin: Optional[str] = Field(alias="productNameThin", default=None)
    category_level1: Optional[str] = Field(alias="categoryLevel1", default=None)
    category_level2: Optional[str] = Field(alias="categoryLevel2", default=None)
    category_level3: Optional[str] = Field(alias="categoryLevel3", default=None)
    category_level4: Optional[str] = Field(alias="categoryLevel4", default=None)
    custom_category_title: Optional[str] = Field(
        alias="customCategoryTitle", default=None
    )
    assortment: Optional[str] = Field(default=None)
    assortment_text: Optional[str] = Field(alias="assortmentText", default=None)
    origin_level1: Optional[str] = Field(alias="originLevel1", default=None)
    origin_level2: Optional[str] = Field(alias="originLevel2", default=None)
    country: Optional[str] = Field(default=None)
    producer_name: Optional[str] = Field(alias="producerName", default=None)
    supplier_name: Optional[str] = Field(alias="supplierName", default=None)
    vintage: Optional[str] = Field(default=None)
    alcohol_percentage: Optional[float] = Field(alias="alcoholPercentage", default=None)
    volume: Optional[int] = Field(default=None)
    volume_text: Optional[str] = Field(alias="volumeText", default=None)
    price: Optional[float] = Field(default=None)
    is_organic: Optional[bool] = Field(alias="isOrganic", default=None)
    is_ethical: Optional[bool] = Field(alias="isEthical", default=None)
    is_kosher: Optional[bool] = Field(alias="isKosher", default=None)
    is_sustainable_choice: Optional[bool] = Field(
        alias="isSustainableChoice", default=None
    )
    bottle_text: Optional[str] = Field(alias="bottleText", default=None)
    seal: Optional[str] = Field(default=None)
    packaging_level1: Optional[str] = Field(alias="packagingLevel1", default=None)
    is_climate_smart_packaging: Optional[bool] = Field(
        alias="isClimateSmartPackaging", default=None
    )
    is_completely_out_of_stock: Optional[bool] = Field(
        alias="isCompletelyOutOfStock", default=None
    )
    is_temporary_out_of_stock: Optional[bool] = Field(
        alias="isTemporaryOutOfStock", default=None
    )
    is_discontinued: Optional[bool] = Field(alias="isDiscontinued", default=None)
    is_supplier_temporary_not_available: Optional[bool] = Field(
        alias="isSupplierTemporaryNotAvailable", default=None
    )
    product_launch_date: Optional[datetime] = Field(
        alias="productLaunchDate", default=None
    )
    sell_start_time: Optional[time] = Field(alias="sellStartTime", default=None)
    is_news: Optional[bool] = Field(alias="isNews", default=None)
    is_web_launch: Optional[bool] = Field(alias="isWebLaunch", default=None)
    sugar_content: Optional[int] = Field(alias="sugarContent", default=None)
    sugar_content_gram_per_100ml: Optional[float] = Field(
        alias="sugarContentGramPer100ml", default=None
    )
    grapes: Optional[List[str]] = Field(default_factory=list)
    usage: Optional[str] = Field(default=None)
    taste: Optional[str] = Field(default=None)
    taste_symbols: Optional[List[str]] = Field(
        alias="tasteSymbols", default_factory=list
    )
    taste_clock_bitterness: Optional[int] = Field(
        alias="tasteClockBitter", default=None
    )
    taste_clock_body: Optional[int] = Field(alias="tasteClockBody", default=None)
    taste_clock_roughness: Optional[int] = Field(
        alias="tasteClockRoughness", default=None
    )
    taste_clock_sweetness: Optional[int] = Field(
        alias="tasteClockSweetness", default=None
    )
    taste_clock_fruitacid: Optional[int] = Field(
        alias="tasteClockFruitacid", default=None
    )
    taste_clock_smokiness: Optional[int] = Field(
        alias="tasteClockSmokiness", default=None
    )
    color: Optional[str] = Field(default=None)
    images: Optional[List[SystembolagetImage]] = Field(default_factory=list)

    @computed_field
    def full_name(self) -> str:
        if self.product_name_thin:
            return f"{self.product_name_thin} {self.product_name_bold}".strip()
        return self.product_name_bold

    @computed_field
    def price_per_liter(self) -> Optional[float]:
        if self.price is not None and self.volume is not None and self.volume != 0:
            return round(self.price / (self.volume / 1000), 2)
        return None

    @computed_field
    def alcohol_per_sek(self) -> Optional[float]:
        if (
            all(
                v is not None
                for v in [self.alcohol_percentage, self.volume, self.price]
            )
            and self.price != 0
        ):
            return round((self.alcohol_percentage / 100) * self.volume / self.price, 3)
        return None

    @computed_field
    def category(self) -> str:
        categories = [
            self.category_level1,
            self.category_level2,
            self.category_level3,
            self.category_level4,
        ]
        return " > ".join([cat for cat in categories if cat])

    @computed_field
    def origin(self) -> str:
        origins = [self.country, self.origin_level1, self.origin_level2]
        return ", ".join([origin for origin in origins if origin])

    class Config:
        populate_by_name = True
