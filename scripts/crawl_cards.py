# scripts/crawl_cards.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection.card_crawler import CardCrawler


def main():
    print("=" * 60)
    print("카드 크롤러")
    print("=" * 60)

    # 테스트 모드 선택
    mode = input("\n모드 선택 (1: 테스트 10개, 2: 전체): ")

    if mode == "1":
        test_mode = True
        test_limit = 10
        print("\n🧪 테스트 모드 선택 (10개 카드만)")
    elif mode == "2":
        test_mode = False
        test_limit = None
        print("\n🚀 전체 크롤링 모드 선택")
    else:
        print("❌ 잘못된 입력입니다.")
        return

    # 카드 타입 선택
    card_type = input("\n크롤링할 카드 종류 (CHK: 체크카드, CRD: 신용카드): ").upper()

    if card_type not in ['CHK', 'CRD']:
        print("❌ 잘못된 입력입니다. CHK 또는 CRD를 입력하세요.")
        return

    # 크롤러 실행
    crawler = CardCrawler()

    try:
        csv_file = crawler.crawl_all_cards(
            card_type=card_type,
            test_mode=test_mode,
            test_limit=test_limit
        )
        print(f"\n✅ 크롤링 완료!")
        print(f"📁 저장 위치: {csv_file}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")

    finally:
        crawler.close()


if __name__ == "__main__":
    main()