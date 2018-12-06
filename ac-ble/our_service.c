
#include <stdint.h>
#include <string.h>
#include "nrf_gpio.h"
#include "our_service.h"
#include "ble_srv_common.h"
#include "app_error.h"
#include "configuration.h"
#include "ac-dimmer.h"

static void on_write(ble_os_t * p_our_service, ble_evt_t const * p_ble_evt)
{
    ble_gatts_evt_write_t const * p_evt_write = &p_ble_evt->evt.gatts_evt.params.write;

    // Custom Value Characteristic Written to.
    if (p_evt_write->handle == p_our_service->char_handles.value_handle)
    {
        uint32_t char_data = *(p_evt_write->data);
        printf("Characteristic written to. Value: 0x%lX (%ld)\n", char_data, char_data);
        
        /* Char data:
         * xxxccsssllllllll
         *
         * l = dim level bit
         * s = source bit
         * c = config bit
         *     - lo bit = motion tracking
         *     - hi bit = light tracking
         * x = not used
         *
         */
        uint8_t new_dim_level = char_data & 0xFF;
        uint8_t source = (char_data >> 8) & 0x7;
        if (new_dim_level != get_dim_level()) {
          set_dim_level(new_dim_level, source);
        }
        motion_tracking_enabled = (char_data >> 11)  & 1;
        light_tracking_enabled = (char_data >> 12) & 1;
    }
    /*
    // Check if the Custom value CCCD is written to and that the value is the appropriate length, i.e 2 bytes.
    if ((p_evt_write->handle == p_our_service->custom_value_handles.cccd_handle)
        && (p_evt_write->len == 2)
       )
    {
        // CCCD written, call application event handler
        if (p_cus->evt_handler != NULL)
        {
            ble_cus_evt_t evt;

            if (ble_srv_is_notification_enabled(p_evt_write->data))
            {
                printf("Notifications enabled\n");
                evt.evt_type = BLE_CUS_EVT_NOTIFICATION_ENABLED;
            }
            else
            {
                printf("Notifications disabled\n");
                evt.evt_type = BLE_CUS_EVT_NOTIFICATION_DISABLED;
            }
            // Call the application event handler.
            p_cus->evt_handler(p_cus, &evt);
        }
    }
    */

}

void ble_our_service_on_ble_evt(ble_evt_t const * p_ble_evt, void * p_context)
{
  	ble_os_t * p_our_service =(ble_os_t *) p_context;
		//Implement switch case handling BLE events related to our service.
           switch (p_ble_evt->header.evt_id)
    {
        case BLE_GAP_EVT_CONNECTED:
          p_our_service->conn_handle = p_ble_evt->evt.gap_evt.conn_handle;
            break;
        case BLE_GAP_EVT_DISCONNECTED:
          UNUSED_PARAMETER(p_ble_evt);
          p_our_service->conn_handle = BLE_CONN_HANDLE_INVALID;
            break;
        case BLE_GATTS_EVT_WRITE:
            on_write(p_our_service, p_ble_evt);
            break;
      default:
          // No implementation needed.
          break;
    }

}

// This Function is for adding our new characterstic to the setvice "lighting".

static uint32_t our_char_add(ble_os_t * p_our_service)
{
    // Adding a custom characteristic UUID
    uint32_t            err_code_brightness_char;
    ble_uuid_t          char_uuid;
    ble_uuid128_t       base_uuid = BLE_UUID_OUR_BASE_UUID;
    char_uuid.uuid      = BLE_UUID_BRIGHTNESS_CHARECTERISTIC;
    err_code_brightness_char = sd_ble_uuid_vs_add(&base_uuid, &char_uuid.type);
    APP_ERROR_CHECK(err_code_brightness_char);






    // Configuring Client Characteristic Configuration Descriptor metadata and add to char_md structure
    ble_gatts_attr_md_t cccd_md;
    memset(&cccd_md, 0, sizeof(cccd_md));

    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&cccd_md.write_perm);
    cccd_md.vloc                = BLE_GATTS_VLOC_STACK;

    //Adding read/write properties to our characteristic
    ble_gatts_char_md_t char_md;
    memset(&char_md, 0, sizeof(char_md));

    char_md.char_props.read = 1;
    char_md.char_props.write = 1;
    char_md.p_cccd_md           = &cccd_md;
    char_md.char_props.notify   = 1;


    // Configuring the attribute metadata
    ble_gatts_attr_md_t attr_md;
    memset(&attr_md, 0, sizeof(attr_md));
    attr_md.vloc        = BLE_GATTS_VLOC_STACK;


    //Setting read/write security levels to our characteristic
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.write_perm);


    //Configuring the characteristic value attribute
    ble_gatts_attr_t    attr_char_value;
    memset(&attr_char_value, 0, sizeof(attr_char_value));

    attr_char_value.p_uuid      = &char_uuid;
    attr_char_value.p_attr_md   = &attr_md;
    attr_char_value.max_len     = 4;
    attr_char_value.init_len    = 4;
    uint8_t value[4]            = {0x00,0x00,0x00,0x00};
    attr_char_value.p_value     = value;


    //Adding our new characteristic to the service
    err_code_brightness_char = sd_ble_gatts_characteristic_add(p_our_service->service_handle,
                                   &char_md,
                                   &attr_char_value,
                                   &p_our_service->char_handles);
    APP_ERROR_CHECK(err_code_brightness_char);

    return NRF_SUCCESS;

    }


// Function for initiating our new service.
 void our_service_init(ble_os_t * p_our_service)
{
    uint32_t   err_code; // Variable to hold return codes from library and softdevice functions

    // Declaring 16-bit service and 128-bit base UUIDs and add them to the BLE stack
    ble_uuid_t        service_uuid;
    ble_uuid128_t     base_uuid = BLE_UUID_OUR_BASE_UUID;
    service_uuid.uuid = BLE_UUID_OUR_SERVICE_UUID;
    err_code = sd_ble_uuid_vs_add(&base_uuid, &service_uuid.type);
    APP_ERROR_CHECK(err_code);

    // Setting our service connection handle to default value. I.e. an invalid handle since we are not yet in a connection.

    p_our_service->conn_handle = BLE_CONN_HANDLE_INVALID;

    // Adding our service
		err_code = sd_ble_gatts_service_add(BLE_GATTS_SRVC_TYPE_PRIMARY,&service_uuid, &p_our_service->service_handle);

    APP_ERROR_CHECK(err_code);

    // Calling the function our_char_add() to add our new characteristic to the service.
    our_char_add(p_our_service);
}

// Function to be called when updating characteristic value
uint32_t our_characteristic_update(ble_os_t *p_our_service, uint16_t level, uint16_t source)
{

  if (p_our_service == NULL)
  {
      return NRF_ERROR_NULL;
  }
  uint32_t char_value = (level & 0xFF) | (source << 8) | (motion_tracking_enabled << 11) | (light_tracking_enabled << 12);

  uint32_t err_code = NRF_SUCCESS;
  ble_gatts_value_t gatts_value;

  // Initialize value struct.
  memset(&gatts_value, 0, sizeof(gatts_value));

  gatts_value.len     = 4;
  gatts_value.offset  = 0;
  gatts_value.p_value = (uint8_t *)&char_value;

  // Update database.
  err_code = sd_ble_gatts_value_set(p_our_service->conn_handle,
                                    p_our_service->char_handles.value_handle,
                                    &gatts_value);
  if (err_code != NRF_SUCCESS)
  {
      return err_code;
  }
    // Updating characteristic value
    if (p_our_service->conn_handle != BLE_CONN_HANDLE_INVALID)
  {
      ble_gatts_hvx_params_t hvx_params;
      memset(&hvx_params, 0, sizeof(hvx_params));

      hvx_params.handle = p_our_service->char_handles.value_handle;
      hvx_params.type   = BLE_GATT_HVX_NOTIFICATION;
      hvx_params.offset = gatts_value.offset;
      hvx_params.p_len  = &gatts_value.len;
      hvx_params.p_data = gatts_value.p_value;

      sd_ble_gatts_hvx(p_our_service->conn_handle, &hvx_params);
    } else {
      err_code = NRF_ERROR_INVALID_STATE;
      //NRF_LOG_INFO("sd_ble_gatts_hvx result: NRF_ERROR_INVALID_STATE. \r\n");
    }

  return err_code;

}