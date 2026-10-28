# 후보 목록과 선정

출처: [darjeeling/awesome-mcp-korea](https://github.com/darjeeling/awesome-mcp-korea) README, 커밋 `23565c02a6556da439c84b29c670a4b00fd1823e` (2026-05-13).
조회일: 2026-10-03. 라이선스·마지막 푸시 날짜는 GitHub REST API (`gh api repos/<repo>`) 응답 그대로입니다.
"키 변수"는 저장소 소스에서 읽는 환경 변수를 검색해 확인했습니다.

선정 기준: 공공기관 API(법령·국회·공시·국세청·관광·통계·국토부·도서관)를 감싸는 서버, stdio 로 실행할 수 있는 서버,
가능하면 라이선스가 명시된 서버. 표본을 10개(변형 1개 별도)로 제한했습니다.

| 저장소 | 목록 분류 | 라이선스 | 마지막 푸시 | 키 변수 | 결과 |
|---|---|---|---|---|---|
| chrisryugj/korean-law-mcp | Legal | MIT | 2026-10-01 | `LAW_OC` | 시험 |
| hollobit/assembly-api-mcp | Legal | MIT | 2026-05-02 | `ASSEMBLY_API_KEY` | 시험 |
| jjlabsio/korea-stock-mcp | Finance | ISC | 2026-10-02 | `DART_API_KEY`, `KRX_API_KEY` | 시험 |
| aesthetic-legalism5470/korean-dart-mcp | Finance | MIT | 2026-10-01 | `DART_API_KEY` | 시험 (처음 고정한 `9631564` 가 같은 날 원격 저장소에서 조회되지 않아 `4b2e072` 로 다시 고정) |
| snaiws/DART-mcp-server | Finance | MIT | 2025-07-07 | `DART_API_KEY` | 시험 |
| Koomook/data-go-mcp-servers (nts-business-verification) | Public Data | Apache-2.0 | 2025-09-16 | `API_KEY` | 시험 (+ `mcp<2` 고정 변형) |
| harimkang/mcp-korea-tourism-api | Tourism | MIT | 2025-08-12 | `KOREA_TOURISM_API_KEY` | 시험 |
| Dayoooun/korea-stats-mcp | Public Data | MIT | 2026-10-01 | `KOSIS_API_KEY` | 시험 |
| tae0y/real-estate-mcp | Real Estate | MIT | 2026-07-18 | `DATA_GO_KR_API_KEY` | 시험 |
| isnow890/data4library-mcp | Public Data | MIT | 2026-09-01 | `LIBRARY_API_KEY` | 시험 |
| aeriis-kr/opendata-mcp (목록 표기 ceami/opendata-mcp) | Public Data | Apache-2.0 | 2026-09-11 | 설정 객체 `ODP_SERVICE_KEY` | 제외: stdio 진입점 없음(Smithery 런타임 전용) |
| worker-ants/korea-weather-mcp | Weather | MIT | 2026-05-13 | `KOREA_WEATHER_API_KEY` | 제외: 표본 제한 |
| ChangooLee/mcp-kr-legislation | Legal | NOASSERTION | 2026-04-28 | - | 검토만 |
| finalchild/law-mcp | Legal | 없음 | 2025-07-07 | - | 검토만 |
| SeoNaRu/korean-law-mcp | Legal | 없음 | 2026-01-20 | - | 검토만 |
| rabqatab/LexLink-ko-mcp | Legal | 없음 | 2026-06-21 | - | 검토만 |
| slicequeue/k-mfds-fooddb-mcp-server | Public Data | 없음 | 2025-08-02 | - | 검토만 |
| slicequeue/k-targo-subway-mcp-server | Public Data | 없음 | 2025-08-02 | - | 검토만 |
| hjsh200219/korea-public-data-mcp | Public Data | 없음 | 2026-09-27 | - | 검토만 |
| jaykim429/korea-statistic-MCP-cginside | Public Data | MIT | 2026-10-02 | - | 검토만(표본 제한) |
| jayjodev/vivory-mcp | Public Data | 없음 | 2026-06-05 | - | 검토만 |
| pinnaclesoft-ko/be-node-seoul-data-mcp | Public Data | MIT | 2025-04-03 | - | 검토만(표본 제한) |
| pjookim/mcp-visit-korea | Tourism | 없음 | 2025-04-10 | - | 검토만 |
| woongaro/KMA-WEATHER-MCP | Weather | 없음 | 2026-01-14 | - | 검토만 |
| ohhan777/korea_weather | Weather | 없음 | 2026-02-22 | - | 검토만 |
| Kinuk97/mcp-get-weather | Weather | 없음 | 2025-06-19 | - | 검토만 |
| jikime/mcp-weather | Weather | 없음 | 2025-04-16 | - | 검토만 |
| dbsxortime/mcp-weather-server | Weather | 없음 | 2025-04-22 | - | 검토만 |
| ChangooLee/mcp-kr-realestate | Real Estate | NOASSERTION | 2026-02-26 | - | 검토만 |

라이선스가 명시되지 않은 저장소는 코드 재사용 조건이 불분명해 표본에서 우선 제외했습니다. 품질과는 무관한 기준입니다.
