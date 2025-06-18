using UnityEngine;

public class PuzzlePieceTransform : MonoBehaviour
{
    public float rotationSpeed = 100f; // Speed of rotation for x, y, and z axes
    public float movementSpeed = 5f; // Speed of movement along the axes

    // Expose keys for rotation in the Inspector
    public KeyCode rotateXKey = KeyCode.UpArrow;  // Key to rotate along the X-axis
    public KeyCode rotateYKey = KeyCode.RightArrow;  // Key to rotate along the Y-axis
    public KeyCode rotateZClockwiseKey = KeyCode.Q;  // Key to rotate along the Z-axis clockwise
    public KeyCode rotateZCounterClockwiseKey = KeyCode.E;  // Key to rotate along the Z-axis counter-clockwise

    // Expose keys for movement in the Inspector
    public KeyCode moveXPositiveKey = KeyCode.D;  // Key to move along the X-axis positive direction
    public KeyCode moveXNegativeKey = KeyCode.A;  // Key to move along the X-axis negative direction
    public KeyCode moveYPositiveKey = KeyCode.Space;  // Key to move along the Y-axis positive direction
    public KeyCode moveYNegativeKey = KeyCode.LeftShift;  // Key to move along the Y-axis negative direction
    public KeyCode moveZPositiveKey = KeyCode.W;  // Key to move along the Z-axis positive direction
    public KeyCode moveZNegativeKey = KeyCode.S;  // Key to move along the Z-axis negative direction

    private bool isSelected = false; // Whether this piece is selected for manipulation

    void Update()
    {
        // Check for selection input (e.g., mouse click) to control this piece
        if (Input.GetMouseButtonDown(0)) // Left click
        {
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit))
            {
                if (hit.transform == transform) // Check if the clicked object is this piece
                {
                    isSelected = !isSelected; // Toggle selection state
                }
            }
        }

        // Only handle movement and rotation if the piece is selected
        if (isSelected)
        {
            HandleRotation();
            HandleMovement();
        }
    }

    void HandleRotation()
    {
        // Rotate piece based on user input
        float rotateX = 0f;
        float rotateY = 0f;
        float rotateZ = 0f;

        // Check for rotation input on X-axis
        if (Input.GetKey(rotateXKey))
        {
            rotateX = rotationSpeed * Time.deltaTime;
        }

        // Check for rotation input on Y-axis
        if (Input.GetKey(rotateYKey))
        {
            rotateY = rotationSpeed * Time.deltaTime;
        }

        // Check for rotation input on Z-axis
        if (Input.GetKey(rotateZClockwiseKey))
        {
            rotateZ = rotationSpeed * Time.deltaTime;
        }
        else if (Input.GetKey(rotateZCounterClockwiseKey))
        {
            rotateZ = -rotationSpeed * Time.deltaTime;
        }

        // Apply rotation to the piece
        transform.Rotate(rotateX, rotateY, rotateZ, Space.Self);
    }

    void HandleMovement()
    {
        // Movement along the X, Y, and Z axes based on user input
        float moveX = 0f;
        float moveY = 0f;
        float moveZ = 0f;

        // Check for movement along the X-axis
        if (Input.GetKey(moveXPositiveKey))
        {
            moveX = movementSpeed * Time.deltaTime;
        }
        else if (Input.GetKey(moveXNegativeKey))
        {
            moveX = -movementSpeed * Time.deltaTime;
        }

        // Check for movement along the Y-axis
        if (Input.GetKey(moveYPositiveKey))
        {
            moveY = movementSpeed * Time.deltaTime;
        }
        else if (Input.GetKey(moveYNegativeKey))
        {
            moveY = -movementSpeed * Time.deltaTime;
        }

        // Check for movement along the Z-axis
        if (Input.GetKey(moveZPositiveKey))
        {
            moveZ = movementSpeed * Time.deltaTime;
        }
        else if (Input.GetKey(moveZNegativeKey))
        {
            moveZ = -movementSpeed * Time.deltaTime;
        }

        // Apply movement to the piece
        transform.Translate(moveX, moveY, moveZ, Space.Self);
    }
}
