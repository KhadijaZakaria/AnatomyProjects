using UnityEngine;

public class PuzzlePieceMovement : MonoBehaviour
{
    private Vector3 offset;
    private bool isBeingDragged = false;
    private Snapping snappingScript;

    // Highlighting
    private Renderer pieceRenderer;
    private Color originalColor;
    public Color highlightColor = Color.yellow; // Customize highlight color in Inspector

    // Rotation speed and movement speed for control
    public float rotationSpeed = 100f; // Speed of rotation for x, y, and z axes
    public float movementSpeed = 5f; // Speed of movement along the axes

    // Expose keys for rotation in the Inspector
    public KeyCode rotateXKey = KeyCode.X;  // Key to rotate along the X-axis
    public KeyCode rotateYKey = KeyCode.Y;  // Key to rotate along the Y-axis
    public KeyCode rotateZClockwiseKey = KeyCode.H;  // Key to rotate along the Z-axis clockwise
    public KeyCode rotateZCounterClockwiseKey = KeyCode.G;  // Key to rotate along the Z-axis counter-clockwise

    // Expose keys for movement in the Inspector
    public KeyCode moveXPositiveKey = KeyCode.RightArrow;  // Key to move along the X-axis positive direction
    public KeyCode moveXNegativeKey = KeyCode.LeftArrow;  // Key to move along the X-axis negative direction
    public KeyCode moveYPositiveKey = KeyCode.UpArrow;  // Key to move along the Y-axis positive direction
    public KeyCode moveYNegativeKey = KeyCode.DownArrow;  // Key to move along the Y-axis negative direction
    public KeyCode moveZPositiveKey = KeyCode.W;  // Key to move along the Z-axis positive direction
    public KeyCode moveZNegativeKey = KeyCode.S;  // Key to move along the Z-axis negative direction

    private bool isSelected = false; // Whether this piece is selected for manipulation

    // Static variable to track the currently dragged piece
    private static PuzzlePieceMovement currentlyDraggedPiece;

    void Start()
    {
        // Get the Snapping script attached to the same GameObject
        snappingScript = GetComponent<Snapping>();
        pieceRenderer = GetComponent<Renderer>();

        if (pieceRenderer != null)
        {
            originalColor = pieceRenderer.material.color; // Store the original color
        }
    }

    void OnMouseDown()
    {
        // Only allow dragging if the piece is not snapped and no other piece is being dragged
        if (snappingScript != null && !snappingScript.isSnapped && currentlyDraggedPiece == null)
        {
            isBeingDragged = true;

            // Set this piece as the currently dragged piece
            currentlyDraggedPiece = this;

            // Calculate the offset between the object's position and the mouse position in world space
            Vector3 mouseWorldPoint = GetMouseWorldPoint();
            offset = transform.position - mouseWorldPoint;

            // Toggle selection state
            isSelected = true;

            // Highlight the piece
            HighlightPiece(true);
        }
    }

    void OnMouseUp()
    {
        // When releasing the mouse, stop dragging and clear the static reference
        if (isBeingDragged)
        {
            isBeingDragged = false;
            currentlyDraggedPiece = null; // Reset the dragged piece reference

            // Remove the highlight
            HighlightPiece(false);
        }
    }

    void HighlightPiece(bool highlight)
    {
        if (pieceRenderer != null && GameManager.isGameActive)
        {
            pieceRenderer.material.color = highlight ? highlightColor : originalColor;
        }
    }
    
    void Update()
    {
        if (isBeingDragged && GameManager.isGameActive)
        {
            // Continuously set the position to the mouse position plus the offset
            Vector3 mouseWorldPoint = GetMouseWorldPoint();
            transform.position = mouseWorldPoint + offset;
        }

        // Only allow rotation and movement if this piece is the one being dragged
        if (isBeingDragged && GameManager.isGameActive)
        {
            HandleRotation();
            HandleMovement();
        }
    }

    // Get the mouse position in world space, maintaining the Z coordinate of the object
    private Vector3 GetMouseWorldPoint()
    {
        Vector3 mousePoint = Input.mousePosition;
        mousePoint.z = Camera.main.WorldToScreenPoint(transform.position).z; // Keep Z position constant
        return Camera.main.ScreenToWorldPoint(mousePoint);
    }

    // Handle piece rotation based on input keys
    void HandleRotation()
    {
        // Rotate piece based on user input only if it's being dragged
        if (currentlyDraggedPiece == this)
        {
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
    }

    // Handle piece movement based on input keys
    void HandleMovement()
    {
        // Movement along the X, Y, and Z axes based on user input only if it's being dragged
        if (currentlyDraggedPiece == this)
        {
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
}
