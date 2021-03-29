class API:
    def __init__(self, attributes = { "version":"1.0" }):
        self.attributes = attributes
        self.accounts = Methods_Accounts(self.attributes)
        self.alerts = Methods_Alerts(self.attributes) 
        self.markets = Methods_Market(self.attributes)
        self.orders = Methods_Orders(self.attributes)
        attributes['consumer_key'] = None
        attributes['consumer_secret'] = None
        attributes['session'] = None
        attributes['last_exception'] = None
        self.status = False

    def jd(self,input_object, indent=4):
        import json
        print(json.dumps(input_object, indent=4))

    def authenticate(self):
        import rauth
        import webbrowser 

        while self.attributes['consumer_key'] is None:
            self.attributes['consumer_key'] = input("Consumer Key not set. Please enter the consumer key: ")
        while self.attributes['consumer_secret'] is None:
            self.attributes['consumer_secret'] = input("Consumer Secret not set. Please enter the consumer key: ")
        ### Modified from https://stackoverflow.com/questions/28579489/getting-an-oauth-request-token-from-etrade-in-python
        service = rauth.OAuth1Service(
                name = 'etrade',
                consumer_key = self.attributes['consumer_key'],
                consumer_secret = self.attributes['consumer_secret'],
                request_token_url = 'https://api.etrade.com/oauth/request_token',
                access_token_url = 'https://api.etrade.com/oauth/access_token',
                authorize_url = 'https://us.etrade.com/e/t/etws/authorize?key={}&token={}',
                base_url = 'https://api.etrade.com')

        oauth_token, oauth_token_secret = service.get_request_token(params =
            {'oauth_callback': 'oob', 
                'format': 'json'})

        auth_url = service.authorize_url.format(self.attributes['consumer_key'], oauth_token)
        
        webbrowser.open(auth_url)
        verifier = input('Please input the verifier: ')
        
        try:
            self.attributes['session'] = service.get_auth_session(oauth_token, oauth_token_secret, params = {'oauth_verifier': verifier})
            self.status = bool(self.attributes['session'].access_token) ##True if auth was successful
            return True
        except:
            print("Error validating verifier token for session. Authentication Failed")
            return False

class Methods_Accounts:
    def __init__(self, attributes):
        self.attributes = attributes
    def list_accounts(self):
        # This API returns a list of E*TRADE accounts for the current user.
        # No Input variables required
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/list'
            url_params = {'format': 'json'}
            resp = self.attributes['session'].get(url, params=url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def get_accounts_balance(self,accountIdKey, instType="BROKERAGE", accountType=None, realTimeNAV='false'):
        # This API retrieves the current account balance and related details for a specified account.
        #Mandatory Input Variables: 
        #   accountIdKey (URL)   - The unique account key. Retrievable by calling the List Accounts API.
        #   instType        - The account institution type for which the balance or information is requested	
        #Optional Input Variables: 
        #   accountType     - The registered account type. See https://apisb.etrade.com/docs/api/account/api-balance-v1.html
        #   realTimeNAV     - Default is false. If true, fetches real time balance	

        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/balance'.format(accountIdKey=accountIdKey)
            
            url_params = {'format': 'json'}

            url_params['instType'] = instType
            url_params['realTimeNAV'] = realTimeNAV

            if accountType: url_params['accountType'] = accountType
            
            resp = self.attributes['session'].get(url, params=url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def list_transactions(self,accountIdKey, startDate=None, endDate=None, marker=None, count=None):
        # The Transaction APIs provide information about transactions for the selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey    - The unique account key. Retrievable by calling the List Accounts API.
        #Optional Input Variables: 
        #   startDate       - The earliest date to include in the date range, formatted as MMDDYYYY. History is available for two years.	
        #   endDate         - The latest date to include in the date range, formatted as MMDDYYYY	
        #   marker          - Specifies the desired starting point of the set of items to return. Used for paging as described in the Notes below.	
        #   count           - Number of transactions to return in the response. If not specified, defaults to 50. Used for paging as described in the Notes below.	

        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/transactions'.format(accountIdKey=accountIdKey)

            url_params = {'format': 'json'}

            if startDate: url_params['startDate'] = startDate
            if endDate: url_params['endDate'] = endDate
            if marker: url_params['marker'] = marker
            if count: url_params['count'] = count
            
            resp = self.attributes['session'].get(url, params=url_params)

            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def list_transaction_details(self,accountIdKey, tranid, storeId=None, startDate=None):
        # Get transaction details for the specified transaction (transactionId). If a transactionId is provided, 
        # no additional path params should be specified in the URI. API should fail with 404 if any path param 
        # is specified after activityId. In order to make requests around the specific break out transaction 
        # types within the Transaction API, simply append the title of the Transaction Category to the end of 
        # the path. This will provide you with only transactions of that type so that you can build functionality 
        # and interact with subsets of data. Possible transaction sub-types include: Trades, Withdrawals, Cash.
        #Mandatory Input Variables: 
        #   accountIdKey    - The unique account key. Retrievable by calling the List Accounts API.
        #   tranid          - 
        #Optional Input Variables: 
        #   storeId       - storage location for older transactions	
      
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/transactions/{tranid}'.format(accountIdKey=accountIdKey, tranid=tranid)

            
            url_params = {'format': 'json'}

            if startDate: url_params['startDate'] = startDate
            if storeId: url_params['storeId'] = storeId
            
            resp = self.attributes['session'].get(url, params=url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def view_portfolio(self,accountIdKey, count=None, sortBy=None, marketSession=None, marker=None ):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey    - The unique account key. Retrievable by calling the List Accounts API.
        #Optional Input Variables: 
        #   count           - The number of positions to return in the response. If not specified, defaults to 50. Used for paging as described in the Notes below.	
        #   sortBy          - The sort by query. Sorting done based on the column specified in the query paramater.	
        #   marketSession   -   The market session. Default: REGULAR	
        #   marker          - Specifies the desired starting point of the set of items to return. Used for paging as described in the Notes below.	

        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/portfolio'.format(accountIdKey=accountIdKey)

            url_params = {'format': 'json'}

            if count: url_params['count'] = count
            if sortBy: url_params['sortBy'] = sortBy
            if marketSession: url_params['marketSession'] = marketSession
            if marker: url_params['marker'] = marker
    
            resp = self.attributes['session'].get(url, params=url_params)
            if len(resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return None
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

class Methods_Market:
    def __init__(self, attributes):
        self.attributes = attributes
    def get_quotes(self,symbols, detailFlag=None, requireEarningsDate=None, overrideSymbolCount=None, skipMiniOptionsCheck=None):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   symbols    -    One or more (comma-separated) symbols for equities or options, up to a maximum of 25. Symbols for equities 
        #                   are simple, for example, GOOG. Symbols for options are more complex, consisting of six elements separated 
        #                   by colons, in this format: underlier:year:month:day:optionType:strikePrice.	
        #Optional Input Variables: 
        #   detailFlag              - Determines the market fields returned from a quote request.	ALL, FUNDAMENTAL, INTRADAY, OPTIONS, WEEK_52, MF_DETAIL
        #   requireEarningsDate     - If value is true, then nextEarningDate will be provided in the output. If value is false or if the field is not passed, nextEarningDate will be returned with no value.	
        #   overrideSymbolCount     - If value is true, then symbolList may contain a maximum of 50 symbols; otherwise, symbolList can only contain 25 symbols.	
        #   skipMiniOptionsCheck    - If value is true, no call is made to the service to check whether the symbol has mini options. If value is false or if the field is not specified, a service call is made to check if the symbol has mini options.	
        #                      
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/market/quote/{symbols}'.format(symbols=symbols)

            url_params = {'format': 'json'}

            if detailFlag: url_params['detailFlag'] = detailFlag
            if requireEarningsDate: url_params['requireEarningsDate'] = requireEarningsDate
            if overrideSymbolCount: url_params['overrideSymbolCount'] = overrideSymbolCount
            if skipMiniOptionsCheck: url_params['skipMiniOptionsCheck'] = skipMiniOptionsCheck

            resp = self.attributes['session'].get(url, params = url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def look_up_product(self,search):
        # This API returns a list of securities of a specified type (e.g., equity stock) based on a full or partial match of any part 
        # of the company name. For instance, a search for "jones" returns a list of securities associated with "Jones Soda Co", 
        # "Stella Jones Inc", and many others. 
        #
        #Mandatory Input Variables: 
        #   search    -     The search request
        #                      
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/market/lookup/{search}'.format(search=search)
            resp = self.attributes['session'].get(url, params = {'format': 'json'})
            if len(resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return None
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def get_options_chain(self,symbol, expiryYear=None, expiryMonth=None, expiryDay=None, strikePriceNear=None, noOfStrikes=None, includeWeekly=None, skipAdjusted=None, optionCategor=None, chainType=None, priceType=None):
        # This API returns a list of option chains for a specific underlying instrument. The request must specify an instrument, 
        # the month the option expires, and whether you are interested in calls, puts, or both. Values returned include the option 
        # pair count and information about each option pair, including the type, call count, symbol, product, date, and strike price..
        #
        #Mandatory Input Variables: 
        #   symbol    -     The market symbol for the instrument; for example, GOOG
        #
        #Optional Input Variables: 
        #   expiryYear      - Indicates the expiry year corresponding to which the optionchain needs to be fetched	
        #   expiryMonth     - Indicates the expiry month corresponding to which the optionchain needs to be fetched	
        #   expiryDay       - Indicates the expiry day corresponding to which the optionchain needs to be fetched	
        #   strikePriceNear - The optionchians fetched will have strike price nearer to this value	
        #   noOfStrikes     - Indicates number of strikes for which the optionchain needs to be fetched	
        #   includeWeekly   - The include weekly options request. Default: false.       Allowed Values: true, false
        #   skipAdjusted    - The skip adjusted request. Default: true.	                Allowed Values: true, false
        #   optionCategor   - The option category. Default: STANDARD.	                Allowed Values: STANDARD, ALL, MINI
        #   chainType       - The type of option chain. Default: CALLPUT.	            Allowed Values: CALL, PUT, CALLPUT
        #   priceType       - The price type. Default: ATNM.	                        Allowed Values: ATNM, ALL
        
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/market/optionchains'
            url_params = {'format': 'json'}
            url_params['symbol'] = symbol
    
            if expiryYear: url_params['expiryYear'] = expiryYear
            if expiryMonth: url_params['expiryMonth'] = expiryMonth
            if expiryDay: url_params['expiryDay'] = expiryDay
            if strikePriceNear: url_params['strikePriceNear'] = strikePriceNear
            if noOfStrikes: url_params['noOfStrikes'] = noOfStrikes
            if includeWeekly: url_params['includeWeekly'] = includeWeekly
            if skipAdjusted: url_params['skipAdjusted'] = skipAdjusted
            if optionCategor: url_params['optionCategor'] = optionCategor
            if chainType: url_params['chainType'] = chainType
            if priceType: url_params['priceType'] = priceType

            resp = self.attributes['session'].get(url, params = url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False

    def get_option_expire_dates(self,symbol, expiryType=None):
        # Returns a list of dates suitable for structuring an option table display. The dates are used to group option data (returned by 
        # the optionchains method) for a specified underlier, creating a table display.
        #
        #Mandatory Input Variables: 
        #   symbol    -     The market symbol for the instrument; for example, GOOG
        #               
        #Optional Input Variables: 
        #   expiryType      - Expiration type of the option	
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/market/optionexpiredate'
            url_params = {'format': 'json'}
            
            if expiryType: url_params['expiryType'] = expiryType

            url_params['symbol'] = symbol
            resp = self.attributes['session'].get(url, params = url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
class Methods_Alerts:
    def __init__(self, attributes):
        self.attributes = attributes
    def list_alerts(self, count=25, category=None, status=None, direction=None, search=None):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   None
        #Optional Input Variables: 
        #   count                   - The alert count. By default it returns 25. Max values that can be returned: 300.
        #   category                - The alert category. By default it will return STOCK and ACCOUNT.
        #   status                  - The alert status. By default it will return READ and UNREAD.
        #   direction               - Sorting is done based on the createDate
        #   search                  - The alert search. Search is done based on the subject.                  
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/user/alerts'
            url_params = {'format': 'json'}
            if count: url_params['count'] = str(count)
            if category: url_params['category'] = category
            if status: url_params['status'] = status
            if direction: url_params['direction'] = direction
            if search: url_params['search'] = search
            resp = self.attributes['session'].get(url, params = url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def list_alert_details(self, id, htmlTags=None):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   id                    - The alert ID value. Alert id whose details are needed
        #Optional Input Variables: 
        #   htmlTags              - The HTML tags on the alert. By default it is false. If set to true, it returns the alert details msgText with html tags.	
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/user/alerts/{id}'.format(id=id)

            url_params = {'format': 'json'}

            if htmlTags: url_params['htmlTags'] = str(htmlTags).lower()
            resp = self.attributes['session'].get(url, params = url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def delete_alert(self, id):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   id                    - Comma separated alertId list to delete
        #Optional Input Variables: 
        #   NONE
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/user/alerts/{id}'.format(id=id)

            url_params = {'format': 'json'}
            resp = self.attributes['session'].delete(url, params = url_params)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
class Methods_Orders:
    def __init__(self, attributes):
        self.attributes = attributes
    def list_orders(self, accountIdKey, marker=None, count=None, status=None, fromDate=None, toDate=None, symbol=None, securityType=None, transactionType=None, marketSession=None):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey          - The unique account key. Retrievable by calling the List Accounts API.
        #Optional Input Variables: 
        #   marker                - Specifies the desired starting point of the set of items to return. Used for paging as described in the Notes below.
        #   count                 - Number of transactions to return in the response. If not specified, defaults to 25 and maximum count is 100. Used for paging as described in the Notes below.
        #   status                - The The status	(OPEN, EXECUTED, CANCELLED, INDIVIDUAL_FILLS, CANCEL_REQUESTED, EXPIRED, REJECTED, PARTIAL, DO_NOT_EXERCISE, DONE_TRADE_EXECUTED)
        #   fromDate              - The earliest date to include in the date range, formatted as MMDDYYYY. History is available for two years. Both fromDate and toDate should be provided, toDate should be greater than fromDate.	
        #   toDate                - The latest date to include in the date range, formatted as MMDDYYYY. Both fromDate and toDate should be provided, toDate should be greater than fromDate.	
        #   symbol                - The market symbol for the security being bought or sold. API supports only 25 symbols seperated by delimiter " , ".
        #   securityType          - The security type (EQ, OPTN, MF, MMF)
        #   transactionType       - Type of transaction (ATNM, BUY, SELL, SELL_SHORT, BUY_TO_COVER, MF_EXCHANGE)
        #   marketSession         - Session in which the equity order will be place	(REGULAR, EXTENDED)
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/orders'.format(accountIdKey=accountIdKey)
            url_params = {'format': 'json'}

            if marker: url_params['marker'] = marker
            if count: url_params['count'] = count
            if status: url_params['status'] = status
            if fromDate: url_params['fromDate'] = fromDate
            if toDate: url_params['toDate'] = toDate
            if symbol: url_params['symbol'] = symbol
            if securityType: url_params['securityType'] = securityType
            if transactionType: url_params['transactionType'] = transactionType
            if marketSession: url_params['marketSession'] = marketSession
            resp = self.attributes['session'].get(url, params = url_params)
            if (resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return {}
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def preview_order(self, accountIdKey, PreviewOrderRequest):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey          - The unique account key. Retrievable by calling the List Accounts API.	
        #   PreviewOrderRequest   - The body of the preview order request	
        #Optional Input Variables: 
        #   NONE
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/orders/preview'.format(accountIdKey=accountIdKey)
            url_post_data = { 'PreviewOrderRequest': PreviewOrderRequest}
            
            resp = self.attributes['session'].post(url, data = url_post_data)
            if (resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return {}
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def place_order(self, accountIdKey, PlaceOrderRequest):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey          - The unique account key. Retrievable by calling the List Accounts API.	
        #   PlaceOrderRequest     - The body of the place order request	
        #Optional Input Variables: 
        #   NONE
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/orders/place'.format(accountIdKey=accountIdKey)
            url_post_data = { 'PlaceOrderRequest': PlaceOrderRequest}
            
            resp = self.attributes['session'].post(url, data = url_post_data)
            return_dict = xmltodict.parse(resp.text)
            return return_dict
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def cancel_order(self, accountIdKey, CancelOrderRequest):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey          - The unique account key. Retrievable by calling the List Accounts API.	
        #   CancelOrderRequest    - The body of the cancel order request	
        #Optional Input Variables: 
        #   NONE
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/orders/cancel'.format(accountIdKey=accountIdKey)
            url_put_data = { 'CancelOrderRequest': CancelOrderRequest}
            
            resp = self.attributes['session'].put(url, data = url_put_data)
            if (resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return {}
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def change_preview_order(self, accountIdKey, orderId, PreviewOrderRequest):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey          - The unique account key. Retrievable by calling the List Accounts API.	
        #   orderId               - The orderid
        #   PreviewOrderRequest   - The body of the preview order request	
        #Optional Input Variables: 
        #   NONE
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/orders/{orderId}/change/preview'.format(accountIdKey=accountIdKey, orderId=orderId)
            url_put_data = { 'PreviewOrderRequest': PreviewOrderRequest}
            
            resp = self.attributes['session'].put(url, data = url_put_data)
            if (resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return {}
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
    def place_changed_order(self, accountIdKey, orderId, PlaceOrderRequest):
        # This API provides portfolio information for a selected brokerage account.
        #Mandatory Input Variables: 
        #   accountIdKey          - The unique account key. Retrievable by calling the List Accounts API.	
        #   orderId               - The orderid
        #   PlaceOrderRequest     - The body of the place changed order request
        #Optional Input Variables: 
        #   NONE
        import sys
        import xmltodict
        try:
            url = 'https://api.etrade.com/v1/accounts/{accountIdKey}/orders/{orderId}/change/place'.format(accountIdKey=accountIdKey, orderId=orderId)
            url_put_data = { 'PlaceOrderRequest': PlaceOrderRequest}
            
            resp = self.attributes['session'].put(url, data = url_put_data)
            if (resp.text):
                return_dict = xmltodict.parse(resp.text)
                return return_dict
            else:
                return {}
        except:
            err_exception = sys.exc_info()
            print("Exception Making API Call",str(err_exception))
            self.attributes['last_exception'] = sys.exc_info()
            return False
