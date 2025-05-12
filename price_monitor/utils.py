import requests
import re

def get_bestbuy_product_data(product_url):
    # Extraire le skuId de l'URL
    match = re.search(r"skuId=(\d+)", product_url)
    if not match:
        print("❌ SKU ID non trouvé dans l'URL")
        return None

    sku_id = match.group(1)

    # Préparer la requête
    api_url = "https://www.bestbuy.com/gateway/graphql"

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.bestbuy.com",
        "Referer": "https://www.bestbuy.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "fr-FR,fr;q=0.9",
    }

    payload = {
        "operationName": "GetCompareProduct",
        "variables": {
            "conditionTilesplacement": "single-compare",
            "conditionTilessite": "dotcom-l",
            "conditionTileslimit": 3,
            "conditionTilesskuId": str(sku_id),
            "conditionTilesinput": {
                "salesChannel": "mobile",
                "planPaidMemberType": ""
            }
        },
        "query": """query GetCompareProduct($conditionTilesplacement: String!, $conditionTilessite: String!, $conditionTileslimit: Int!, $conditionTilesskuId: String!, $conditionTilesinput: ProductItemPriceInput!) {
    productBySkuId(skuId: $conditionTilesskuId) {
        description {
        long
        __typename
        }
        name {
        short
        __typename
        }
        primaryImage {
        piscesHref
        __typename
        }
        price(input: $conditionTilesinput) {
        currentPrice
        customerPrice
        isMAP
        icrCode
        strictMapIcr
        mobileContracts {
            id
            isDefaultContract
            numberOfPayments
            purchaseType
            termDuration
            termUnits
            currentPrice
            __typename
            carrierCode
        }
        __typename
        }
        reviewInfo {
        averageRating
        reviewCount
        conFeatures {
            name
            __typename
        }
        proFeatures {
            name
            __typename
        }
        __typename
        }
        specificationGroups {
        name
        specifications {
            definition
            displayName
            value
            __typename
        }
        __typename
        }
        url {
        relativePdp
        __typename
        }
        skuId
        __typename
        openBoxCondition
    }
    recommendations(
        filter: {placement: $conditionTilesplacement, site: $conditionTilessite, limit: $conditionTileslimit, skus: [$conditionTilesskuId]}
    ) {
        subPlacements {
        recommendations {
            ep
            id
            item {
            ... on Product {
                primaryImage {
                piscesHref
                __typename
                }
                url {
                relativePdp
                __typename
                }
                description {
                long
                __typename
                }
                name {
                short
                __typename
                }
                price(input: $conditionTilesinput) {
                currentPrice
                customerPrice
                isMAP
                icrCode
                strictMapIcr
                mobileContracts {
                    id
                    isDefaultContract
                    numberOfPayments
                    purchaseType
                    termDuration
                    termUnits
                    currentPrice
                    __typename
                    carrierCode
                }
                __typename
                }
                reviewInfo {
                averageRating
                reviewCount
                conFeatures {
                    name
                    __typename
                }
                proFeatures {
                    name
                    __typename
                }
                __typename
                }
                specificationGroups {
                name
                specifications {
                    definition
                    displayName
                    value
                    __typename
                }
                __typename
                }
                skuId
                __typename
                openBoxCondition
            }
            __typename
            }
            __typename
        }
        ep
        id
        name
        __typename
        }
        __typename
    }
    __typename
    }"""
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        product = result["data"]["productBySkuId"]
        Titre = product['name']['short']
        price = product["price"]["customerPrice"]

        print(f"✅ Titre : {Titre}")
        print(f"💰 Prix client : {price}")

        return {
            "Titre": Titre,
            "price": price
        }

    except Exception as e:
        print("❌ Erreur :", e)
        print("Réponse brute :", response.text[:500])
        return None

# if __name__ == "__main__":
#     product_url = "https://www.bestbuy.com/site/acer-aspire-5-15-6-laptop-amd-ryzen-5-7535u-8gb-memory-amd-radeon-graphics-512gb-ssd/6572161.p?skuId=6572161"
#     get_bestbuy_product_data(product_url)